PACKAGE_VERSION := $(shell poetry version --short)
IMAGE := $(IMAGE_REPO)/moldock:$(PACKAGE_VERSION)

build:
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)

format:
	black moldock/


run:
	uvicorn moldock.main:app --reload
