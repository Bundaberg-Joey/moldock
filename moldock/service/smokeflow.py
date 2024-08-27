from metaflow import FlowSpec, step


class SmokeFlow(FlowSpec):
    @step
    def start(self):
        import os

        self.exit_status = str(os.system("smina --version"))

        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    SmokeFlow()
