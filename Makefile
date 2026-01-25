ORG ?= roswellcityuk
REGISTRY ?= ghcr.io/$(ORG)

.PHONY: setup-builder clean build-% push-% test-%

# Create a buildx builder instance if one doesn't exist (useful for local multi-arch simulation)
setup-builder:
	docker buildx inspect dev-builder > /dev/null 2>&1 || docker buildx create --name dev-builder --use

# Build using buildx (loads the image into local docker daemon so you can run it immediately)
build-%: setup-builder
	$(eval VERSION := $(shell cat images/$*/VERSION))
	docker buildx build --load \
		--platform linux/amd64,linux/arm64 \
		-t $(REGISTRY)/toolchain-$*:$(VERSION) \
		-t $(REGISTRY)/toolchain-$*:latest \
		images/$*

push-%:
	$(eval VERSION := $(shell cat images/$*/VERSION))
	docker push $(REGISTRY)/toolchain-$*:$(VERSION)
	docker push $(REGISTRY)/toolchain-$*:latest

clean:
	docker buildx rm dev-builder || true