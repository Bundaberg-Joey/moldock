import os
import time

from metaflow import Runner
from metaflow import Flow

from moldock.service import smokeflow, workflow
from moldock.utils import execute_cli_command


class DockingSimulation:

    def __init__(self, server: str):
        self.base_command = F'python3 {workflow.__file__}' 
        
        if server == "local":
            self.base_command += ' --environment local'
        elif server == "aws_batch":
            self.base_command += ' '
        else:
            raise ValueError(
                f"Only `local` and `aws_batch` servers permitted. Got {server} instead."
            )
        self.base_command += ' run'

    def dock_ligands(self, receptor_path: str, ligand_path: str, s3_root: str):
        execute_cli_command(F'{self.base_command} --recept_path {receptor_path} --ligand_path {ligand_path} --s3_root {s3_root}')
        
        run = Flow('DockingFlow').latest_run
        while not run.finished:
            print('Waiting for docking flow to finish')
            time.sleep(10)
        return run.data.results_path if run.successful else None


def run_smoketest():
    execute_cli_command(f"python3 {smokeflow.__file__} --environment local run")
    expected_result = "Smina Oct 15 2019.  Based on AutoDock Vina 1.1.2."

    run = Flow("SmokeFlow").latest_run
    result = run.data.result if run.successful else "Workflow Failed To Execute, No `data` artifacts available."
    return result, expected_result, str(run.finished_at)
