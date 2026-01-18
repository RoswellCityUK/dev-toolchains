ORG ?= roswellcityuk
REGISTRY ?= ghcr.io/$(ORG)

# Use a pattern rule (%) to handle any image folder in images/
build-%:
	$(eval VERSION := $(shell cat images/$*/VERSION))
	docker build -t $(REGISTRY)/toolchain-$*:$(VERSION) images/$*
	docker tag $(REGISTRY)/toolchain-$*:$(VERSION) $(REGISTRY)/toolchain-$*:latest

push-%:
	$(eval VERSION := $(shell cat images/$*/VERSION))
	docker push $(REGISTRY)/toolchain-$*:$(VERSION)
	docker push $(REGISTRY)/toolchain-$*:latest

test-%:
	$(eval VERSION := $(shell cat images/$*/VERSION))
	# A simple sanity check to ensure the image runs
	docker run --rm $(REGISTRY)/toolchain-$*:$(VERSION) sh -c "cat /etc/os-release"