IMAGE := $(IMAGE_REPO)/$(IMAGE_NAME):$(VERSION_TAG)

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
