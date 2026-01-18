ORG ?= roswellcityuk
REGISTRY ?= ghcr.io/$(ORG)

LATEX_IMAGE := $(REGISTRY)/toolchain-latex
LATEX_VERSION := $(shell cat images/latex/VERSION)

.PHONY: latex-build latex-push latex-test

latex-build:
	docker build -t $(LATEX_IMAGE):texlive-2024.$(LATEX_VERSION) images/latex
	docker tag $(LATEX_IMAGE):texlive-2024.$(LATEX_VERSION) $(LATEX_IMAGE):texlive-2024
	docker tag $(LATEX_IMAGE):texlive-2024.$(LATEX_VERSION) $(LATEX_IMAGE):latest

latex-push:
	docker push $(LATEX_IMAGE):texlive-2024.$(LATEX_VERSION)
	docker push $(LATEX_IMAGE):texlive-2024
	docker push $(LATEX_IMAGE):latest

latex-test:
	docker run --rm $(LATEX_IMAGE):texlive-2024.$(LATEX_VERSION) latexmk -v
	docker run --rm $(LATEX_IMAGE):texlive-2024.$(LATEX_VERSION) biber --version
