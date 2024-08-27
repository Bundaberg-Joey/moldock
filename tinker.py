from metaflow import Flow

run = Flow('SmokeFlow').latest_run
print(run.tags)