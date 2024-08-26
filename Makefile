IMAGE := $(IMAGE_REPO)/$(IMAGE_NAME):$(VERSION_TAG)

build:
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)

format:
	black moldock/


run:
	docker compose up -d 
