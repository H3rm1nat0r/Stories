import json
import logging

from nemo_library.nemo_library import NemoLibrary
from nemo_library.utils.utils import FilterType, FilterValue

PROJECT_NAME = "Business Processes"


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
nl = NemoLibrary()
nl.MetaDataLoad(
    projectname=PROJECT_NAME,
    filter="optimate_",
    filter_type=FilterType.STARTSWITH,
    filter_value=FilterValue.INTERNALNAME,
)
