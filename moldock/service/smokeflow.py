from metaflow import FlowSpec, step


class SmokeFlow(FlowSpec):
    @step
    def start(self):
        from moldock.utils import execute_cli_command

        stdout, stderr = execute_cli_command("smina --version", error_as_stderr=True)
        self.result = stdout.strip() + stderr.strip()

        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    SmokeFlow()
