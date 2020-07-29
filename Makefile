BIN ?= nauticock
SRCDIR ?= nauticock
BLDDIR ?= build
PYTHON ?= /usr/bin/env python3
REQLIST ?= make_requirements.txt

.DEFAULT_GOAL := $(BLDDIR)/$(BIN)

$(BLDDIR)/$(BIN): $(SRCDIR)/**/*.py
	rm -rf $(BLDDIR)/$(BIN)
	mkdir -p $(BLDDIR)/$(BIN)
	cp -r --no-preserve=ownership $(SRCDIR) $(BLDDIR)/$(BIN)/$(BIN)
	mv $(BLDDIR)/$(BIN)/$(BIN)/__main__.py $(BLDDIR)/$(BIN)/__main__.py
	$(PYTHON) -m pip install -r $(REQLIST) --target $(BLDDIR)/$(BIN) --no-deps
	find $(BLDDIR)/$(BIN) -name '__pycache__' -exec rm -rf '{}' +
	find $(BLDDIR)/$(BIN) -name '*.dist-info' -exec rm -rf '{}' +
	find $(BLDDIR)/$(BIN) -exec touch -t 198001011200 '{}' \;
	$(PYTHON) -m zipapp -p '$(PYTHON)' $(BLDDIR)/$(BIN)
	rm -rf $(BLDDIR)/$(BIN)
	mv $(BLDDIR)/$(BIN).pyz $(BLDDIR)/$(BIN)

build: $(BLDDIR)/$(BIN)

clean:
	rm -rf $(BLDDIR)

.PHONY: build clean
