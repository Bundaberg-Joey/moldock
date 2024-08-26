from fastapi import APIRouter

from moldock.http_api.dto import DockingJobRequest, DockingJobResult
from moldock.service.interface import DockingSimulation

route = APIRouter()


@route.post("/dock/", response_model=DockingJobResult)
async def predict(body: DockingJobRequest):
    docker = DockingSimulation(server=body.server)
    results_filepath = docker.dock_ligands(
        receptor_path=body.receptor_path,
        ligand_path=body.ligand_path,
        s3_root=body.s3_root,
    )
    return {"results_filepath": results_filepath, "message": "Docking complete"}
