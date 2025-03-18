from configparser import ConfigParser
import logging
from nemo_library import NemoLibrary

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

PROJECT_NAME = "Business Processes"
customers = ["amf", "pirlo", "emz", "wipotec"]

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
    nl.MetaDataDelete(projectname=PROJECT_NAME, prefix="(Conservative)")
    nl.MetaDataDelete(projectname=PROJECT_NAME, prefix="(C)")
    nl.MetaDataCreate(projectname=PROJECT_NAME, prefix="(C)")
