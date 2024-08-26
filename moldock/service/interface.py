import time

from metaflow import Runner, Flow

from moldock.service import workflow


class DockingSimulation:

    def __init__(self, server: str):
        self.runner_kwargs = {"flow_file": workflow.__file__, "show_output": True}

        if server == "local":
            server_kwargs = {"environment": "local"}
        elif server == "aws_batch":
            server_kwargs = {}
        else:
            raise ValueError(
                f"Only `local` and `aws_batch` servers permitted. Got {server} instead."
            )

        self.runner_kwargs = {**self.runner_kwargs, **server_kwargs}

    def dock_ligands(self, receptor_path: str, ligand_path: str, s3_root: str):
        with Runner(**self.runner_kwargs).run(
            receptor_path=receptor_path, ligand_path=ligand_path, s3_root=s3_root
        ) as latest_run:

            while not latest_run.finished:
                print("Waiting for docking flow to finish")
                time.sleep(10)
            return latest_run.data.results_path
