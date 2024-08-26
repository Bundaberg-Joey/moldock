from fastapi import APIRouter

from moldock.http_api.dto import DockingJobRequest, DockingJobResult
from moldock.service.interface import LocalDockingSoftware, AwsBatchDockingSoftware


DockingFlows = {
    "local": LocalDockingSoftware,
    "batch": AwsBatchDockingSoftware,
}


route = APIRouter()


@route.post("/dock/", response_model=DockingJobResult)
async def predict(body: DockingJobRequest):
    docker = DockingFlows[body.server]()
    results_filepath = docker.dock_ligands(
        receptor_path=body.receptor_path, ligand_path=body.ligand_path
    )
    return {"results_filepath": results_filepath, "message": "Docking complete"}
