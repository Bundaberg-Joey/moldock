from datetime import datetime

from fastapi import APIRouter

from moldock.http_api.dto import DockingJobRequest, DockingJobResult, SmokeTestResult
from moldock.service.interface import DockingSimulation, run_smoketest

route = APIRouter()


@route.post("/dock/", response_model=DockingJobResult)
def predict(body: DockingJobRequest):
    docker = DockingSimulation(server=body.server)
    results_filepath = docker.dock_ligands(
        receptor_path=body.receptor_path,
        ligand_path=body.ligand_path,
        s3_root=body.s3_root,
    )
    return {"results_filepath": results_filepath, "message": "Docking complete"}


@route.get("/healthcheck/")
def health_check():
    return {"message": f"Service Reachable as of {datetime.now()}"}


@route.get("/smoketest/", response_model=SmokeTestResult)
def smoke_test():
    result, expected_result, finished_at = run_smoketest()
    return {
        "message": "smoke test complete",
        "finished_at": finished_at,
        "result": result,
        "expected_result": expected_result,
        "smoketest_pass": result == expected_result,
    }
