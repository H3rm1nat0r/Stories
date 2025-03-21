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
    path = Path(".") / "metadata_optimate_purchasing" / f"{file}.json"
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
            "optimate_purchasing_"
        ), f"internal name does not start with optimate_purchasing_: {application.internalName}"
        assert "en" in application.displayNameTranslations, f"displayNameTranslations does not contain 'en': {application.internalName}"    
        assert "de" in application.displayNameTranslations, f"displayNameTranslations does not contain 'de': {application.internalName}"    
        
        assert application.displayName == application.displayNameTranslations["en"], f"displayName is not equal to displayNameTranslations['en']: {application.internalName}"

def test_attributegroups():
    for attributegroup in attributegroups:
        assert attributegroup.internalName.startswith(
            "optimate_purchasing_"
        ), f"internal name does not start with optimate_purchasing_: {attributegroup.internalName}"
        assert "en" in attributegroup.displayNameTranslations, f"displayNameTranslations does not contain 'en': {attributegroup.internalName}"    
        assert "de" in attributegroup.displayNameTranslations, f"displayNameTranslations does not contain 'de': {attributegroup.internalName}"    
        
        assert attributegroup.displayName == attributegroup.displayNameTranslations["en"], f"displayName is not equal to displayNameTranslations['en']: {attributegroup.internalName}"

def test_pages():
    for page in pages:
        assert page.internalName.startswith(
            "optimate_purchasing_"
        ), f"internal name does not start with optimate_purchasing_: {page.internalName}"
        assert "en" in page.displayNameTranslations, f"displayNameTranslations does not contain 'en': {page.internalName}"    
        assert "de" in page.displayNameTranslations, f"displayNameTranslations does not contain 'de': {page.internalName}"    
        
        assert page.displayName == page.displayNameTranslations["en"], f"displayName is not equal to displayNameTranslations['en']: {page.internalName}"

applications = _load_data_from_json("applications", Application)
attributegroups = _load_data_from_json("attributegroups", AttributeGroup)
defined_columns = _load_data_from_json("definedcolumns", DefinedColumn)
metrics = _load_data_from_json("metrics", Metric)
pages = _load_data_from_json("pages", Page)
