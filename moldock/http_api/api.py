from datetime import datetime

from fastapi import APIRouter

from moldock.http_api.dto import DockingJobRequest, DockingJobResult, SmokeTestResult, SmokeFlowRequest
from moldock.service.interface import DockingSimulation, run_smoketest

route = APIRouter()


@route.post("/dock/", response_model=DockingJobResult)
def predict(body: DockingJobRequest):
    docker = DockingSimulation(server=body.server)
    results_filepath = docker.dock_ligands(
        uniprot_id=body.uniprot_id,
        ligand_path=body.ligand_path,
        s3_root=body.s3_root,
    )
    return {"results_filepath": results_filepath, "message": "Docking complete"}


@route.get("/healthcheck/")
def health_check():
    return {"message": f"Service Reachable as of {datetime.now()}"}


@route.post("/smoketest/", response_model=SmokeTestResult)
def smoke_test(body: SmokeFlowRequest):
    exit_status, finished_at = run_smoketest(server=body.server)
    return {
        "message": "smoke test complete",
        "finished_at": finished_at,
        "exit_status": exit_status,
        "smoketest_pass": exit_status == "0",
    }
