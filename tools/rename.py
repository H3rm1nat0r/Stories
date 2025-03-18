import json
import logging
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


def _get_internal_name(displayname: str) -> str:
    internal_name = displayname.replace("(C)", "conservative")
    internal_name = internal_name.replace("Purch", "purchasing")
    internal_name = internal_name.replace(" ", "_")
    internal_name = internal_name.replace("-", "")
    internal_name = internal_name.replace("(", "")
    internal_name = internal_name.replace(")", "")
    internal_name = internal_name.lower()
    return internal_name


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


path = Path(".") / "metadata_conservative" / "metrics.json"

metrics = _load_data_from_json("metrics", Metric)
pages = _load_data_from_json("pages", Page)
definedcolumns = _load_data_from_json("definedcolumns", DefinedColumn)

for metric in metrics:
    metric.displayName = metric.displayName.replace("  ", " ")
    internal_name = _get_internal_name(metric.displayName)
    if internal_name != metric.internalName:
        logging.info(f"Replacing {metric.internalName} with {internal_name}")
        for page in pages:
            for visual in page.visuals:
                if metric.internalName in visual.content:
                    visual.content = visual.content.replace(
                        metric.internalName, internal_name
                    )

        metric.internalName = internal_name

for defined_column in definedcolumns:
    defined_column.displayName = defined_column.displayName.replace("  ", " ")
    internal_name = _get_internal_name(defined_column.displayName)
    if internal_name != defined_column.internalName:
        logging.info(
            f"Replacing '{defined_column.internalName}' with '{internal_name}'"
        )
        for defined_column_relation in definedcolumns:
            if defined_column.internalName in defined_column_relation.formula:
                defined_column_relation.formula = (
                    defined_column_relation.formula.replace(
                        defined_column.internalName, internal_name
                    )
                )
        for metric in metrics:
            if defined_column.internalName in metric.aggregateBy:
                metric.aggregateBy = metric.aggregateBy.replace(
                    defined_column.internalName, internal_name
                )
            if defined_column.internalName in metric.aggregateFunction:
                metric.aggregateFunction = metric.aggregateFunction.replace(
                    defined_column.internalName, internal_name
                )
            for groupByAggregation in list(metric.groupByAggregations.keys()):
                if defined_column.internalName in groupByAggregation:
                    new_groupByAggregation = groupByAggregation.replace(
                        defined_column.internalName, internal_name
                    )
                    metric.groupByAggregations[new_groupByAggregation] = (
                        metric.groupByAggregations.pop(groupByAggregation)
                    )
        defined_column.internalName = internal_name

_export_data_to_json("metrics", metrics)
_export_data_to_json("pages", pages)
_export_data_to_json("definedcolumns", definedcolumns)
