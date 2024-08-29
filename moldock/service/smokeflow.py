from metaflow import FlowSpec, step, batch


class SmokeFlow(FlowSpec):
    
    @batch(image='crh201/moldock:latest', cpu=1)
    @step
    def start(self):
        import os

        self.exit_status = str(os.system("smina --version"))

        self.next(self.end)

    @batch(image='crh201/moldock:latest', cpu=1)
    @step
    def end(self):
        pass


if __name__ == "__main__":
    SmokeFlow()
