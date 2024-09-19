image = 'crh201/moldock:latest'

docking_resources = F' --with batch:cpu=2,queue=default,image={image}'
smokeflow_resources = F' --with batch:cpu=1,queue=default,image={image}'