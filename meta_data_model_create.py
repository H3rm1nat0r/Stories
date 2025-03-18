import logging
import pandas as pd

from nemo_library.nemo_library import NemoLibrary

PROJECT_NAME = "Business Processes"

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
nl = NemoLibrary()
nl.MetaDataCreate(projectname=PROJECT_NAME,prefix="(C)")
