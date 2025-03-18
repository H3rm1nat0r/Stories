import json
import logging

from nemo_library.nemo_library import NemoLibrary
from nemo_library.utils.utils import FilterType

PROJECT_NAME = "Business Processes"


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
nl = NemoLibrary()
nl.MetaDataDelete(projectname=PROJECT_NAME,prefix="(Conservative)")
nl.MetaDataDelete(projectname=PROJECT_NAME,prefix="(C)")
