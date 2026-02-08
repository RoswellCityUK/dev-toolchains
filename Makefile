ORG ?= roswellcityuk
REGISTRY ?= ghcr.io/$(ORG)

.PHONY: setup-builder clean build-% push-% test-%

setup-builder:
	docker buildx inspect dev-builder > /dev/null 2>&1 || docker buildx create --name dev-builder --use

build-%: setup-builder
	$(eval VERSION := $(shell cat images/$*/VERSION))
	docker buildx build --load \
		--platform linux/amd64 \
		-t $(REGISTRY)/toolchain-$*:$(VERSION) \
		-t $(REGISTRY)/toolchain-$*:latest \
		images/$*

push-%: build-%
	$(eval VERSION := $(shell cat images/$*/VERSION))
	docker push $(REGISTRY)/toolchain-$*:$(VERSION)
	docker push $(REGISTRY)/toolchain-$*:latest

clean:
	docker buildx rm dev-builder || true