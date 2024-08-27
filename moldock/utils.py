import subprocess


class CliExecutionError(Exception):
    pass


def execute_cli_command(command: str, error_as_stderr=False, **kwargs):
    try:
        process_result = subprocess.run(str(command).split(), **kwargs)
    except (
        subprocess.TimeoutExpired,
        subprocess.CalledProcessError,
        FileNotFoundError,
    ) as e:
        if error_as_stderr:
            return "", str(e)
        raise CliExecutionError(f"{command} failed to run : {e}")

    if kwargs.get("capture_output", False):
        return [
            r.decode("utf-8") for r in (process_result.stdout, process_result.stderr)
        ]
