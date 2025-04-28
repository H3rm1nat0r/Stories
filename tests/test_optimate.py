import json
from pathlib import Path
from typing import Any, List, Type, TypeVar, get_type_hints
from nemo_library.model.application import Application
from nemo_library.model.attribute_group import AttributeGroup
from nemo_library.model.defined_column import DefinedColumn
from nemo_library.model.metric import Metric
from nemo_library.model.pages import Page

T = TypeVar("T")

COCKPIT = "optimate"


def _load_data_from_json(file: str, cls: Type[T]) -> List[T]:
    """
    Loads JSON data from a file and converts it into a list of DataClass instances,
    handling nested structures recursively.
    """
    path = Path(".") / f"metadata_{COCKPIT}" / f"{file}.json"
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


def _generic_test(items):
    for item in items:
        assert item.internalName.startswith(
            COCKPIT
        ), f"internal name of item does not start with {COCKPIT}: {item.internalName}"
        assert (
            "en" in item.displayNameTranslations
        ), f"displayNameTranslations of item does not contain 'en': item {item.internalName}"
        assert (
            "de" in item.displayNameTranslations
        ), f"displayNameTranslations of item does not contain 'de': item {item.internalName}"

        assert (
            item.displayName == item.displayNameTranslations["en"]
        ), f"displayName is not equal to displayNameTranslations['en']: {item.internalName}"

def test_applications():
    _generic_test(applications)


def test_attributegroups():
    _generic_test(attributegroups)


def test_pages():
    _generic_test(pages)


def test_definedcolumns():
    _generic_test(definedcolumns)

    #check if all defined columns are used in a metric
    for definedcolumn in definedcolumns:    
        found = False
        for metric in metrics:
            if definedcolumn.internalName in metric.aggregateBy:
                found = True
                break
            if definedcolumn.internalName in metric.aggregateFunction:
                found = True
                break
            if definedcolumn.internalName in metric.groupByAggregations.keys():
                found = True
                break
        
        # or in another defined column
        for definedcolumn2 in definedcolumns:
            if definedcolumn.internalName in definedcolumn2.formula:
                found = True
                break
            
        assert found, f"defined column {definedcolumn.internalName} is not used in a metric nor another defined column"

def test_metrics():
    _generic_test(metrics)

    # Check internal names
    for metric in metrics:

        if metric.dateColumn != "pur_order_doc_date":
            assert (
                False
            ), f"found purchasing metric that does not have pur_order_doc_date as date column: {metric.internalName}"
        if metric.groupByColumn != "pur_order_doc_i_d":
            assert (
                False
            ), f"found purchasing metric that does not have pur_order_doc_i_d as group by column: {metric.internalName}"
            
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


applications = _load_data_from_json("applications", Application)
attributegroups = _load_data_from_json("attributegroups", AttributeGroup)
definedcolumns = _load_data_from_json("definedcolumns", DefinedColumn)
metrics = _load_data_from_json("metrics", Metric)
pages = _load_data_from_json("pages", Page)
