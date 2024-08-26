from metaflow import  Runner


from moldock.service import workflow



with Runner(workflow.__name__, show_output=True, environment='local').run() as running:
    print(f'{running.run} completed on Kubernetes!')