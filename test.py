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
metrics = nl.getMetrics(
    projectname=PROJECT_NAME,
)

for metric in metrics:
    if metric.displayNameTranslations:
        print(json.dumps(metric.to_dict(),indent=4))
        exit()