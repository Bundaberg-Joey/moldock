import os
import time

from metaflow import Run

from moldock.service import smokeflow, workflow
from moldock.service.utils import launch_metaflow_workflow
from moldock.utils import execute_cli_command


class DockingSimulation:

    def __init__(self, server: str):
        self.base_command = f"python3 {workflow.__file__}"

        if server == "local":
            self.base_command += " --environment local"
        elif server == "aws_batch":
            self.base_command += " "
        else:
            raise ValueError(
                f"Only `local` and `aws_batch` servers permitted. Got {server} instead."
            )
        self.base_command += " run"

    def dock_ligands(self, receptor_path: str, ligand_path: str, s3_root: str):
        run_id = launch_metaflow_workflow(
            f"{self.base_command} --recept_path {receptor_path} --ligand_path {ligand_path} --s3_root {s3_root}"
        )
        run = Run(f"DockingFlow/{run_id}")
        while not run.finished:
            print("Waiting for docking flow to finish")
            time.sleep(10)
        return run.data.results_path if run.successful else None


def run_smoketest():
    run_id = launch_metaflow_workflow(
        f"python3 {smokeflow.__file__} --environment local run"
    )
    run = Run(f"SmokeFlow/{run_id}")
    exit_status = (
        run.data.exit_status
        if run.successful
        else "Workflow Failed To Execute, No `data` artifacts available."
    )
    return exit_status, str(run.finished_at)
