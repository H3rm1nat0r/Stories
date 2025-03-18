import json
from pathlib import Path
from typing import Any, List, Type, TypeVar, get_type_hints
from nemo_library.model.application import Application
from nemo_library.model.attribute_group import AttributeGroup
from nemo_library.model.defined_column import DefinedColumn
from nemo_library.model.metric import Metric
from nemo_library.model.pages import Page

T = TypeVar("T")


def _load_data_from_json(file: str, cls: Type[T]) -> List[T]:
    """
    Loads JSON data from a file and converts it into a list of DataClass instances,
    handling nested structures recursively.
    """
    path = Path(".") / "metadata_conservative" / f"{file}.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [_deserializeMetaDataObject(item, cls) for item in data]


def _deserializeMetaDataObject(value: Any, target_type: Type) -> Any:
    """
    Recursively deserializes JSON data into a nested DataClass structure.
    """
    if isinstance(value, list):
        # Check if we expect a list of DataClasses
        if hasattr(target_type, "__origin__") and target_type.__origin__ is list:
            element_type = target_type.__args__[0]
            return [_deserializeMetaDataObject(v, element_type) for v in value]
        return value  # Regular list without DataClasses
    elif isinstance(value, dict):
        # Check if the target type is a DataClass
        if hasattr(target_type, "__annotations__"):
            field_types = get_type_hints(target_type)
            return target_type(
                **{
                    key: _deserializeMetaDataObject(value[key], field_types[key])
                    for key in value
                    if key in field_types
                }
            )
        return value  # Regular dictionary
    return value  # Primitive values


def _export_data_to_json(file: str, data):
    path = Path(".") / "metadata_conservative" / f"{file}.json"
    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            [element.to_dict() for element in data], file, indent=4, ensure_ascii=True
        )


def test_metrics():

    # Check display names
    for metric in metrics:
        assert (
            "  " not in metric.displayName
        ), f"found double space in metric: {metric.displayName}"
        assert metric.displayName.startswith(
            "(C)"
        ), f"metric does not start with (C): {metric.displayName}"

    # Check internal names
    for metric in metrics:

        # Check if internal name starts with conservative_
        assert metric.internalName.startswith(
            "conservative_"
        ), f"internal name does not start with conservative_: {metric.internalName}"

        # Check if second part of internal name is either purchasing or sales
        assert metric.internalName.split("_")[1] in [
            "purchasing",
            "sales",
        ], f"second part of internal name is not purchasing or sales: {metric.internalName}"

        # Check if internal name matches display name
        internal_name = metric.displayName.replace("(C)", "conservative")
        internal_name = internal_name.replace("Purch", "purchasing")
        internal_name = internal_name.replace(" ", "_")
        internal_name = internal_name.replace("(", "")
        internal_name = internal_name.replace(")", "")
        internal_name = internal_name.lower()
        assert (
            metric.internalName == internal_name
        ), f"internal name does not match: {metric.internalName} != {internal_name}"

    # Check if all metrics are part of a visual
    metrics_in_visuals = [visual.content for page in pages for visual in page.visuals]
    split_metrics_in_visuals = []  # some visuals have multiple metrics
    for item in metrics_in_visuals:
        split_metrics_in_visuals.extend(item.split(","))

    split_metrics_in_visuals = list(set(split_metrics_in_visuals))

    for metric in metrics:
        if metric.internalName not in split_metrics_in_visuals:
            assert (
                False
            ), f"found metric that is not part of a visual: {metric.internalName}"

    # special checks for purchasing metrics
    purchasing_metrics = [
        metric
        for metric in metrics
        if metric.internalName.split("_")[1] == "purchasing"
    ]
    for metric in purchasing_metrics:
        if metric.dateColumn != "pur_order_doc_date":
            assert (
                False
            ), f"found purchasing metric that does not have pur_order_doc_date as date column: {metric.internalName}"
        if metric.groupByColumn != "pur_order_doc_i_d":
            assert (
                False
            ), f"found purchasing metric that does not have pur_order_doc_i_d as group by column: {metric.internalName}"

    # special checks for sales metrics
    sales_metrics = [
        metric for metric in metrics if metric.internalName.split("_")[1] == "sales"
    ]
    for metric in sales_metrics:
        if metric.dateColumn != "invoice_doc_date":
            assert (
                False
            ), f"found sales metric that does not have invoice_doc_date as date column: {metric.internalName}"
        if metric.groupByColumn != "invoice_doc_i_d":
            assert (
                False
            ), f"found sales metric that does not have invoice_doc_i_d as group by column: {metric.internalName}"


path = Path(".") / "metadata_conservative" / "metrics.json"

application = _load_data_from_json("applications", Application)
attribute_groups = _load_data_from_json("attributegroups", AttributeGroup)
defined_columns = _load_data_from_json("definedcolumns", DefinedColumn)
metrics = _load_data_from_json("metrics", Metric)
pages = _load_data_from_json("pages", Page)
