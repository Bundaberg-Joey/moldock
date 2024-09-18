IMAGE := crh201/moldock:latest

build:
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)

format:
	black moldock/

clean:
	rm -rf .metaflow

local:
	uvicorn moldock.http_api.main:app

run:
	docker compose up -d 
