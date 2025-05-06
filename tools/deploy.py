from configparser import ConfigParser
import logging
from nemo_library import NemoLibrary
from nemo_library.utils.utils import FilterType, FilterValue

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

PROJECT_NAME = "Business Processes"
customers = [
    "amf",
    "pirlo",
    "emz",
    "wipotec",
    "proalpha",
]

for customer in customers:
    logging.info(f"Deploying {customer}")

    config = ConfigParser()
    config.read("config.ini")
    tenant = config.get(f"nemo_library_{customer}", "tenant", fallback=None)
    userid = config.get(f"nemo_library_{customer}", "userid", fallback=None)
    password = config.get(f"nemo_library_{customer}", "password", fallback=None)
    environment = config.get(f"nemo_library_{customer}", "environment", fallback=None)

    nl = NemoLibrary(
        tenant=tenant,
        userid=userid,
        password=password,
        environment=environment,
    )
    nl.MetaDataDelete(
        projectname=PROJECT_NAME,
        filter="(Conservative)",
        filter_type=FilterType.STARTSWITH,
        filter_value=FilterValue.DISPLAYNAME,
    )
    nl.MetaDataDelete(
        projectname=PROJECT_NAME,
        filter="(C)",
        filter_type=FilterType.STARTSWITH,
        filter_value=FilterValue.DISPLAYNAME,
    )
    nl.MetaDataDelete(
        projectname=PROJECT_NAME,
        filter="optimate",
        filter_type=FilterType.STARTSWITH,
        filter_value=FilterValue.INTERNALNAME,
    )

    # nl = NemoLibrary(
    #     tenant=tenant,
    #     userid=userid,
    #     password=password,
    #     environment=environment,
    #     metadata="./metadata_optimate_purchasing"
    # )
    # nl.MetaDataCreate(
    #     projectname=PROJECT_NAME,
    #     filter="optimate_purchasing",
    #     filter_type=FilterType.STARTSWITH,
    #     filter_value=FilterValue.DISPLAYNAME,
    # )

    # nl = NemoLibrary(
    #     tenant=tenant,
    #     userid=userid,
    #     password=password,
    #     environment=environment,
    #     metadata="./metadata_optimate_global"
    # )
    # nl.MetaDataCreate(
    #     projectname=PROJECT_NAME,
    #     filter="optimate_global",
    #     filter_type=FilterType.STARTSWITH,
    #     filter_value=FilterValue.DISPLAYNAME,
    # )
