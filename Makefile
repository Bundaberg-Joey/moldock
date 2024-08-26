PACKAGE_VERSION := $(shell poetry version --short)
IMAGE := $(IMAGE_REPO)/moldock:$(PACKAGE_VERSION)

build:
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)

format:
	black moldock/


run:
	docker compose up -d 
