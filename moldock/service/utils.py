import os
from uuid import uuid4

from moldock.utils import execute_cli_command


def launch_metaflow_workflow(metaflow_cli_command):
    metaflow_cli_command = metaflow_cli_command.rstrip()  # remove any trailing space

    if " run " not in metaflow_cli_command and " run" not in metaflow_cli_command:
        raise ValueError("Command must include the `run` flag.")

    tmp_name = f"tmp_{uuid4()}.txt"
    execute_cli_command(metaflow_cli_command + f" --run-id-file {tmp_name}")
    run_id = open(tmp_name, "r").read()
    os.remove(tmp_name)
    return run_id
