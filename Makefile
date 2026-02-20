# ==== CONFIG ====
CONFIG_PATH := isds.yaml
EDGELIST_PATH := topology.txt
TOPOLOGIES_PATH := topologies

CONFIG_MK := .isd-vars.mk

.PHONY: $(CONFIG_MK)
$(CONFIG_MK):
	@python3 scripts/parse-isd-config.py $(CONFIG_PATH) > $(CONFIG_MK)

-include $(CONFIG_MK)

VERSION := 1.0
DEBIAN_DOCKER_DIR = $(CURDIR)

.PHONY: all build rebuild build-debian-base build-base \
        build-scion rebuild-scion rebuild-base rebuild-monitor \
        up down purge show-config

show-config:
	@echo "ISDs: $(ISDS)"
	@echo "ISD1 AS Range: $(ISD1_AS_RANGE)"
	@echo "ISD1 AS Count: $(ISD1_AS_COUNT)"
	@echo "ISD2 AS Range: $(ISD2_AS_RANGE)"
	@echo "Total ASes: $(TOTAL_AS_COUNT)"

all: up

build-debian-base:
	cd "$(DEBIAN_DOCKER_DIR)" && docker build -t debian-systemd:$(VERSION) .

build-base: build-debian-base
	docker build -t scion-base:$(VERSION) \
		-f ./base/Dockerfile \
		.

build-scion:
	@i=1; \
	$(foreach isd,$(ISDS), \
		$(foreach as,$(ISD$(isd)_AS_RANGE), \
			echo ">>> Building SCION node ISD=$(isd) AS=$(as) INDEX=$$i"; \
			docker build \
				-t scion$(isd)$(as):$(VERSION) \
				--build-arg INDEX=$$i \
				--build-arg ISD=$(isd) \
				--build-arg AS=$(as) \
				-f ./template/Dockerfile .; \
			i=$$((i+1)); \
		) \
	)

build-endhost%:
	@as=$*; \
	docker build -t endhost-as$$as:$(VERSION) \
		-f ./endhosts/endhost-as$$as/Dockerfile \
		./endhosts/endhost-as$$as

build-all-endhost: build-endhost15 build-endhost35


build-monitor: generate-nodeconfig 
	docker build -t monitor:$(VERSION) \
		-f ./monitor/Dockerfile \
		./monitor

build: generate-compose generate-topologies build-base build-monitor build-scion build-all-endhost

rebuild: generate-compose generate-topologies rebuild-base rebuild-monitor rebuild-scion

rebuild-base:
	docker build --no-cache -t debian-systemd:$(VERSION) .
	docker build --no-cache -t scion-base:$(VERSION) \
		-f ./base/Dockerfile \
		.

rebuild-scion:
	@i=1; \
	$(foreach isd,$(ISDS), \
		$(foreach as,$(ISD$(isd)_AS_RANGE), \
			echo ">>> Building SCION node ISD=$(isd) AS=$(as) INDEX=$$i"; \
			docker build --no-cache --progress=plain \
				-t scion$(isd)$(as):$(VERSION) \
				--build-arg INDEX=$$i \
				--build-arg ISD=$(isd) \
				--build-arg AS=$(as) \
				-f ./template/Dockerfile .; \
			i=$$((i+1)); \
		) \
	)


rebuild-monitor: generate-nodeconfig
	cd ./monitor/scionctl && GOOS=linux GOARCH=amd64 go build -o scionctl .
	docker build --no-cache -t monitor:$(VERSION) \
		-f ./monitor/Dockerfile \
		./monitor

generate-compose:
	python3 scripts/generate-compose.py \
		--config $(CONFIG_PATH) \
		--version $(VERSION)

generate-topologies:
	python3 scripts/generate-topologies.py \
		--edges $(EDGELIST_PATH) \
		--isds $(CONFIG_PATH) \
		--output-dir $(TOPOLOGIES_PATH)

generate-nodeconfig:
	python3 scripts/generate-nodeconfig.py --config $(CONFIG_PATH)

#install bats shell testing framework
install-bats:
	@if command -v bats >/dev/null 2>&1; then \
		echo "Bats is already installed at $$(command -v bats)"; \
		bats --version; \
	else \
		echo "Cloning bats-core repository..."; \
		git clone https://github.com/bats-core/bats-core.git; \
		echo "Installing bats..."; \
		cd bats-core && sudo ./install.sh /usr/local; \
		rm -rf bats-core; \
		echo "Checking bats installation..."; \
		if command -v bats >/dev/null 2>&1; then \
			echo "Bats installed successfully at $$(command -v bats)"; \
			bats --version; \
		else \
			echo "Bats installation failed or bats is not on your PATH."; \
			exit 1; \
		fi; \
	fi

#run test scripts

OS := $(shell uname)
up: build
ifeq ($(OS), Linux)
	docker compose up -d
else
	docker compose -f docker-compose.yml -f docker-compose.mac.yml up -d
endif

down:
	docker compose down

purge: down
	docker ps -aq --filter "name=scion" | xargs -r docker rm -f
	docker network ls -q --filter "name=^as_net_" --filter "name=^transit_net" | xargs -r docker network rm

.PHONY: test

test: install-bats
	bats test/