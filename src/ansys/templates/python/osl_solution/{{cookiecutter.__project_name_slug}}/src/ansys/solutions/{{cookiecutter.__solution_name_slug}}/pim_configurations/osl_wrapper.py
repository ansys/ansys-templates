# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

from ansys.optislang.core import Optislang
from fastapi import FastAPI, Body

app = FastAPI()

@app.post("/start")
async def start_instance(project_path: str = Body(...), project_properties_file: str = Body(...)):
    global TCP_SERVER_PORT
    osl = Optislang(
        project_path=project_path,
        reset=True,
        shutdown_on_finished=False,
        import_project_properties_file=project_properties_file,
        ini_timeout=300
    )
    # Get server host
    tcp_server_host = osl.get_osl_server().get_host()
    # Get server port
    server_info = osl.get_osl_server().get_server_info()
    tcp_server_port = server_info["server"]["server_port"]
    TCP_SERVER_PORT = tcp_server_port
    return {"host": tcp_server_host, "port": tcp_server_port}


@app.get("/")
async def connect_to_instance():
    return {"port": TCP_SERVER_PORT}

@app.get("/health")
async def health():
    return "healthy"
