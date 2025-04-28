import json
from pathlib import Path
from typing import Any, List, Type, TypeVar, get_type_hints
from nemo_library.model.application import Application
from nemo_library.model.attribute_group import AttributeGroup
from nemo_library.model.defined_column import DefinedColumn
from nemo_library.model.metric import Metric
from nemo_library.model.pages import Page    
from nemo_library.model.attribute_link import AttributeLink
from nemo_library.model.diagram import Diagram
from nemo_library.model.report import Report
from nemo_library.model.rule import Rule
from nemo_library.model.subprocess import SubProcess
from nemo_library.model.tile import Tile

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

def _export_data_to_json(file: str, data):
    path = Path(".") / "metadata_optimate" / f"{file}.json"
    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            [element.to_dict() for element in data], file, indent=4, ensure_ascii=True
        )

path = Path(".") / "metadata_optimate" / "metrics.json"

applications = _load_data_from_json("applications", Application)
attributegroups = _load_data_from_json("attributegroups", AttributeGroup)
attributelinks = _load_data_from_json("attributelinks", AttributeLink)
definedcolumns = _load_data_from_json("definedcolumns", DefinedColumn)
diagrams = _load_data_from_json("diagrams", Diagram)
metrics = _load_data_from_json("metrics", Metric)
pages = _load_data_from_json("pages", Page)
reports = _load_data_from_json("reports", Report)
rules = _load_data_from_json("rules", Rule)
subprocesses = _load_data_from_json("subprocesses", SubProcess)
tiles = _load_data_from_json("tiles", Tile)

for objects in [applications, attributegroups, attributelinks, definedcolumns, diagrams, pages, reports, rules, subprocesses, tiles]:
    for obj in objects:
        if hasattr(obj, "displayNameTranslations"):
            obj.displayName = obj.displayNameTranslations.get("en", obj.displayName)
        if hasattr(obj, "descriptionTranslations"):
            obj.description = obj.descriptionTranslations.get("en", obj.description)

_export_data_to_json("applications", applications)
_export_data_to_json("attributegroups", attributegroups)
_export_data_to_json("attributelinks", attributelinks)
_export_data_to_json("definedcolumns", definedcolumns)
_export_data_to_json("diagrams", diagrams)
_export_data_to_json("metrics", metrics)
_export_data_to_json("pages", pages)
_export_data_to_json("reports", reports)
_export_data_to_json("rules", rules)
_export_data_to_json("subprocesses", subprocesses)
_export_data_to_json("tiles", tiles)    


