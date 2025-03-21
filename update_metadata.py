import logging
from pathlib import Path

from nemo_library.nemo_library import NemoLibrary
from nemo_library.utils.utils import FilterType, FilterValue

PROJECT_NAME = "Business Processes"


class UpdateMetadata:
    def getNemoLibrary(self, cockpit):
        metadata_path = Path(f"./metadata_{cockpit}")
        
        # Create the metadata directory if it does not exist
        metadata_path.mkdir(parents=True, exist_ok=True)
        
        nl = NemoLibrary(metadata=str(metadata_path))
        return nl

    def MetaDataCreate(self, cockpit):
        nl = self.getNemoLibrary(cockpit)
        nl.MetaDataCreate(
            projectname=PROJECT_NAME,
            filter=cockpit,
            filter_type=FilterType.STARTSWITH,
            filter_value=FilterValue.INTERNALNAME,
        )

    def MetaDataDelete(self, cockpit):
        nl = self.getNemoLibrary(cockpit)
        nl.MetaDataDelete(
            projectname=PROJECT_NAME,
            filter=cockpit,
            filter_type=FilterType.STARTSWITH,
            filter_value=FilterValue.INTERNALNAME,
        )

    def MetaDataLoad(self, cockpit):
        nl = self.getNemoLibrary(cockpit)
        nl.MetaDataLoad(
            projectname=PROJECT_NAME,
            filter=cockpit,
            filter_type=FilterType.STARTSWITH,
            filter_value=FilterValue.INTERNALNAME,
        )


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

um = UpdateMetadata()
um.MetaDataCreate("optimate_purchasing")
# um.MetaDataCreate("optimate_global")

# um.MetaDataLoad("optimate_purchasing")
# um.MetaDataLoad("optimate_sales")
# um.MetaDataLoad("optimate_global")

# um.MetaDataDelete("conservative")