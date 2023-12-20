# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

from ansys.optislang.core import Optislang, utils, logging
from pathlib import Path
from fastapi import Body, FastAPI


OSL_SERVER_PORT = None


app = FastAPI()


@app.post("/start")
async def start_instance(project_path: str = Body(...), project_properties_file: str = Body(...), osl_version: int = Body(...), loglevel: str = Body(...)):
    global OSL_SERVER_PORT
    osl = Optislang(
        project_path=project_path,
        executable=utils.get_osl_exec(osl_version)[1],
        loglevel=loglevel,
        reset=True,
        auto_relocate=True,
        shutdown_on_finished=False,
        import_project_properties_file=project_properties_file,
        ini_timeout=300
    )
    # Configure logging.
    osl_logger = logging.OslLogger(
        loglevel=loglevel,
        log_to_file=True,
        logfile_name=Path(project_path).parent / "optiSLang.log",
        log_to_stdout=True,
    )
    osl.__logger = osl_logger.add_instance_logger(osl.name, osl, loglevel)
    osl.log.info("Start instance")
    # Get server host
    osl_server_host = osl.get_osl_server().get_host()
    # Get server port
    server_info = osl.get_osl_server().get_server_info()
    osl_server_port = server_info["server"]["server_port"]
    OSL_SERVER_PORT = osl_server_port
    return {"host": osl_server_host, "port": osl_server_port}


@app.get("/")
async def get_port():
    return {"port": OSL_SERVER_PORT}


@app.get("/health")
async def health():
    return "healthy"
