import os
import time

from metaflow import Run

from moldock.service import smokeflow, workflow
from moldock.service.utils import launch_metaflow_workflow
from moldock.service.resources import smokeflow_resources, docking_resources


def _build_command(path: str, server: str, batch_resources: str) -> str:
    command = F'python3 {path} run'
    if server == 'local':
        resources = ''
    elif server == 'aws_batch':
        resources = batch_resources
    else:
        raise ValueError(
            f"Only `local` and `aws_batch` servers permitted. Got {server} instead."
        )
    return command + resources


class DockingSimulation:

    def __init__(self, server: str):
        self.base_command = _build_command(workflow.__file__, server, docking_resources)

    def dock_ligands(self, uniprot_id: str, ligand_path: str, s3_root: str):
        run_id = launch_metaflow_workflow(
            f"{self.base_command} --uniprot_id {uniprot_id} --ligand_path {ligand_path} --s3_root {s3_root}"
        )
        run = Run(f"DockingFlow/{run_id}")
        while not run.finished:
            print("Waiting for docking flow to finish")
            time.sleep(10)
        return run.data.results_path if run.successful else None


def run_smoketest(server: str):
    command = _build_command(smokeflow.__file__, server, smokeflow_resources)
        
    run_id = launch_metaflow_workflow(command)
    run = Run(f"SmokeFlow/{run_id}")
    exit_status = (
        run.data.exit_status
        if run.successful
        else "Workflow Failed To Execute, No `data` artifacts available."
    )
    return exit_status, str(run.finished_at)
