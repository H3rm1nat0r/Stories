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
    path = Path(".") / "metadata_optimate" / f"{file}.json"
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

def test_applications():
    for application in applications:
        assert application.internalName.startswith(
            "optimate_"
        ), f"internal name does not start with optimate_: {application.internalName}"
        assert "en" in application.displayNameTranslations, f"displayNameTranslations does not contain 'en': {application.internalName}"    
        assert "de" in application.displayNameTranslations, f"displayNameTranslations does not contain 'de': {application.internalName}"    
        
        assert application.displayName == application.displayNameTranslations["en"], f"displayName is not equal to displayNameTranslations['en']: {application.internalName}"

# def test_attribute_groups():
#     for attribute_group in attribute_groups:
#         assert attribute_group.internalName.startswith(
#             "optimate_"
#         ), f"internal name does not start with optimate_: {attribute_group.internalName}"
#         assert "en" in attribute_group.displayNameTranslations, f"displayNameTranslations does not contain 'en': {attribute_group.internalName}"    
#         assert "de" in attribute_group.displayNameTranslations, f"displayNameTranslations does not contain 'de': {attribute_group.internalName}"    
        
#         assert attribute_group.displayName == attribute_group.displayNameTranslations["en"], f"displayName is not equal to displayNameTranslations['en']: {attribute_group.internalName}"

def test_pages():
    for page in pages:
        assert page.internalName.startswith(
            "optimate_"
        ), f"internal name does not start with optimate_: {page.internalName}"
        assert "en" in page.displayNameTranslations, f"displayNameTranslations does not contain 'en': {page.internalName}"    
        assert "de" in page.displayNameTranslations, f"displayNameTranslations does not contain 'de': {page.internalName}"    
        
        assert page.displayName == page.displayNameTranslations["en"], f"displayName is not equal to displayNameTranslations['en']: {page.internalName}"
        
def test_metrics():

    # Check internal names
    for metric in metrics:

        # Check if internal name starts with conservative_
        assert metric.internalName.startswith(
            "optimate_"
        ), f"internal name does not start with optimate_: {metric.internalName}"

        # Check if second part of internal name is either purchasing or sales
        assert metric.internalName.split("_")[1] in [
            "purchasing",
            "sales",
        ], f"second part of internal name is not purchasing or sales: {metric.internalName}"

        assert metric.internalName.startswith(
            "optimate_"
        ), f"internal name does not start with optimate_: {metric.internalName}"
        assert "en" in metric.displayNameTranslations, f"displayNameTranslations does not contain 'en': {metric.internalName}"    
        assert "de" in metric.displayNameTranslations, f"displayNameTranslations does not contain 'de': {metric.internalName}"    
        
        assert metric.displayName == metric.displayNameTranslations["en"], f"displayName is not equal to displayNameTranslations['en']: {application.internalName}"

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

applications = _load_data_from_json("applications", Application)
attribute_groups = _load_data_from_json("attributegroups", AttributeGroup)
defined_columns = _load_data_from_json("definedcolumns", DefinedColumn)
metrics = _load_data_from_json("metrics", Metric)
pages = _load_data_from_json("pages", Page)
