import json
from pathlib import Path
from typing import Any, List, Type, TypeVar, get_type_hints
from nemo_library.model.application import Application
from nemo_library.model.attribute_group import AttributeGroup
from nemo_library.model.defined_column import DefinedColumn
from nemo_library.model.metric import Metric
from nemo_library.model.pages import Page

T = TypeVar("T")

COCKPIT = "optimate_purchasing"


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


def test_applications():
    for application in applications:
        assert application.internalName.startswith(
            COCKPIT
        ), f"internal name of application does not start with {COCKPIT}: {application.internalName}"
        assert (
            "en" in application.displayNameTranslations
        ), f"displayNameTranslations of application does not contain 'en': application {application.internalName}"
        assert (
            "de" in application.displayNameTranslations
        ), f"displayNameTranslations of application does not contain 'de': application {application.internalName}"

        assert (
            application.displayName == application.displayNameTranslations["en"]
        ), f"displayName is not equal to displayNameTranslations['en']: {application.internalName}"

        assert application.internalName == application.displayName.lower().replace(
            " ", "_"
        ), f"internalName is not equal to {application.displayName.lower().replace(" ", "_")}: {application.internalName}"


def test_attributegroups():
    for attributegroup in attributegroups:
        assert attributegroup.internalName.startswith(
            COCKPIT
        ), f"internal name of attributegroup does not start with {COCKPIT}: {attributegroup.internalName}"
        assert (
            "en" in attributegroup.displayNameTranslations
        ), f"displayNameTranslations of attributegroup does not contain 'en': attributegroup {attributegroup.internalName}"
        assert (
            "de" in attributegroup.displayNameTranslations
        ), f"displayNameTranslations of attributegroup does not contain 'de': attributegroup {attributegroup.internalName}"

        assert (
            attributegroup.displayName == attributegroup.displayNameTranslations["en"]
        ), f"displayName is not equal to displayNameTranslations['en']: {attributegroup.internalName}"

        if "(Parking Lot)" in attributegroup.displayName:
            assert (
                "parking_lot" in attributegroup.internalName
            ), f"internalName does not contain 'parking_lot': {attributegroup.internalName}"


def test_pages():
    for page in pages:
        assert page.internalName.startswith(
            COCKPIT
        ), f"internal name of page does not start with {COCKPIT}: {page.internalName}"
        assert (
            "en" in page.displayNameTranslations
        ), f"displayNameTranslations of page does not contain 'en': page {page.internalName}"
        assert (
            "de" in page.displayNameTranslations
        ), f"displayNameTranslations of page does not contain 'de': page {page.internalName}"

        assert (
            page.displayName == page.displayNameTranslations["en"]
        ), f"displayName is not equal to displayNameTranslations['en']: {page.internalName}"


def test_metrics():

    # Check internal names
    for metric in metrics:

        assert metric.internalName.startswith(
            COCKPIT 
        ), f"internal name of metric does not start with {COCKPIT}: {metric.internalName}"
        assert (
            "en" in metric.displayNameTranslations
        ), f"displayNameTranslations of metric does not contain 'en': metric {metric.internalName}"
        if not metric.displayName.startswith("(Parking Lot)"):
            assert (
                "de" in metric.displayNameTranslations
            ), f"displayNameTranslations of metric does not contain 'de': metric {metric.internalName}"

        assert (
            metric.displayName == metric.displayNameTranslations["en"]
        ), f"displayName is not equal to displayNameTranslations['en']: {metric.internalName}"

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
defined_columns = _load_data_from_json("definedcolumns", DefinedColumn)
metrics = _load_data_from_json("metrics", Metric)
pages = _load_data_from_json("pages", Page)
