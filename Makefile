ORG ?= roswellcityuk
REGISTRY ?= ghcr.io/$(ORG)

# Create a buildx builder instance if one doesn't exist (useful for local multi-arch simulation)
setup-builder:
	docker buildx inspect dev-builder > /dev/null 2>&1 || docker buildx create --name dev-builder --use

# Build using buildx (loads the image into local docker daemon so you can run it immediately)
build-%: setup-builder
	$(eval VERSION := $(shell cat images/$*/VERSION))
	docker buildx build --load \
		-t $(REGISTRY)/toolchain-$*:$(VERSION) \
		-t $(REGISTRY)/toolchain-$*:latest \
		images/$*

push-%:
	$(eval VERSION := $(shell cat images/$*/VERSION))
	docker push $(REGISTRY)/toolchain-$*:$(VERSION)
	docker push $(REGISTRY)/toolchain-$*:latest

test-%:
	$(eval VERSION := $(shell cat images/$*/VERSION))
	@echo "Testing $(REGISTRY)/toolchain-$*:$(VERSION)..."
	docker run --rm $(REGISTRY)/toolchain-$*:$(VERSION) \
		bash -c "latexmk -v && biber -v && pygmentize -V"
	docker run --rm $(REGISTRY)/toolchain-$*:$(VERSION) \
		bash -c "echo '\documentclass{article}\begin{document}Hello\end{document}' > test.tex && pdflatex test.tex"
	@echo "✅ All Tests Passed."

clean:
	docker buildx rm dev-builder || true