# ==== CONFIG ====
TOPOLOGY_FILE := topologies/topo0/topo0_it0.yaml
TOPOLOGY_FOLDER := topologies
RESULTS_PATH := topologies/results/results.csv
CONTAINER_TOPOLOGIES_PATH := container-topolgies/
PLOTS_FOLDER := topologies/plots/
SHOWPATHS_PATH := topologies/results/show_paths

CONFIG_MK := .isd-vars.mk

.PHONY: $(CONFIG_MK)
$(CONFIG_MK):
	@python3 scripts/parse-isd-config.py $(TOPOLOGY_FILE) > $(CONFIG_MK)

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
		--build-arg TOPOLOGY_FILE=$(TOPOLOGY_FILE) \
		-f ./base/Dockerfile \
		.

build-scion:
	@i=1; \
	$(foreach isd,$(ISDS), \
		$(foreach as,$(ISD$(isd)_AS_RANGE), \
			echo ">>> Building SCION node ISD=$(isd) AS=$(as) INDEX=$$i"; \
			docker build \
				-t scion$(isd)-$(as):$(VERSION) \
				--build-arg INDEX=$$i \
				--build-arg ISD=$(isd) \
				--build-arg AS=$(as) \
				--build-arg CONTAINER_TOPOLOGIES=$(CONTAINER_TOPOLOGIES_PATH) \
				-f ./template/Dockerfile .; \
			i=$$((i+1)); \
		) \
	)

build-endhost%:
	@id=$*; \
	isd=$${id%-*}; \
	as=$${id#*-}; \
	docker build -t endhost-as$$isd-$$as:$(VERSION) \
		-f ./endhosts/endhost-as$$isd-$$as/Dockerfile \
		./endhosts/endhost-as$$isd-$$as

build-all-endhost: build-endhost1-5 build-endhost3-5


build-monitor: generate-nodeconfig generate-web-ui
	docker build -t monitor:$(VERSION) \
		-f ./monitor/Dockerfile \
		./monitor

build: generate-compose generate-topologies build-base build-monitor build-scion generate-tests 

rebuild: generate-compose generate-topologies rebuild-base rebuild-monitor rebuild-scion generate-tests 

rebuild-base:
	docker build --no-cache -t debian-systemd:$(VERSION) .
	docker build --no-cache -t scion-base:$(VERSION) \
		--build-arg TOPOLOGY_FILE=$(TOPOLOGY_FILE) \
		-f ./base/Dockerfile \
		.

rebuild-scion:
	@i=1; \
	$(foreach isd,$(ISDS), \
		$(foreach as,$(ISD$(isd)_AS_RANGE), \
			echo ">>> Building SCION node ISD=$(isd) AS=$(as) INDEX=$$i"; \
			docker build --no-cache --progress=plain \
				-t scion$(isd)-$(as):$(VERSION) \
				--build-arg INDEX=$$i \
				--build-arg ISD=$(isd) \
				--build-arg AS=$(as) \
				--build-arg CONTAINER_TOPOLOGIES=$(CONTAINER_TOPOLOGIES_PATH) \
				-f ./template/Dockerfile .; \
			i=$$((i+1)); \
		) \
	)

rebuild-monitor: generate-nodeconfig generate-web-ui
	cd ./monitor/scionctl && GOOS=linux GOARCH=amd64 go build -o scionctl .
	docker build --no-cache -t monitor:$(VERSION) \
		-f ./monitor/Dockerfile \
		./monitor

generate-compose:
	python3 scripts/generate-compose.py \
		--config $(TOPOLOGY_FILE) \
		--version $(VERSION)

generate-topologies:
	python3 scripts/generate-topologies.py \
		-tp $(TOPOLOGY_FILE) \
		--output-dir $(CONTAINER_TOPOLOGIES_PATH)

generate-nodeconfig:
	python3 scripts/generate-nodeconfig.py --config $(TOPOLOGY_FILE)

generate-tests:
	python3 scripts/generate-tests.py --config $(TOPOLOGY_FILE)

generate-web-ui:
	python3 scripts/generate-web-ui.py \
		--config $(TOPOLOGY_FILE) \
		--template monitor/index-template.html \
		--output monitor/index.html

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

run-topology-optimizer: topo-optim topo-eval topo-plot

# TOPO_OPTIM_FOLDERS := topo1

# topo-optim:
# 	@for topo in $(TOPO_OPTIM_FOLDERS); do \
# 		file=$$(ls configurations/$$topo/*_it0.yaml) ; \
# 		python3 scripts/rewire_spectral.py -tc $$file ; \
# 		python3 scripts/rewire_np.py -tc $$file ; \
# 	done

topo-optim:
	@for topo in $(TOPOLOGY_FOLDER)/*/; do \
		file=$$(ls $$topo*_it0.yaml) ; \
		python3 scripts/rewire_spectral.py -tc $$file ; \
		python3 scripts/rewire_np.py -tc $$file ; \
	done

topo-eval: 
	python3 scripts/evaluate_topology.py -i $(TOPOLOGY_FOLDER) -o $(RESULTS_PATH); \

topo-plot:
	python3 scripts/plot_topology.py \
	-i $(RESULTS_PATH) \
	-g "^([^_]+)" \
	-sg "_([^_]+)_" \
	-m "cheeger_constant" "spectral_gap" "algebraic_connectivity" \
	-s topology \
	-o $(PLOTS_FOLDER) \
	-t $(TOPOLOGY_FOLDER)

run-path-evaluation:
	@for topo in $(TOPOLOGY_FOLDER)/topo*/; do \
		for file in $$topo*_it*.yaml; do \
			echo ">>> Running path evaluation for $$file"; \
			$(MAKE) rebuild TOPOLOGY_FILE=$$file; \
			$(MAKE) up TOPOLOGY_FILE=$$file; \
			sleep 60; \
			$(MAKE) show-paths TOPOLOGY_FILE=$$file; \
			$(MAKE) down; \
		done; \
	done

show-paths:
	python3 scripts/show_paths.py --config $(TOPOLOGY_FILE) --output-path $(SHOWPATHS_PATH); \

eval-paths:
	python3 scripts/evaluate_paths.py --folder $(SHOWPATHS_PATH) --topologies $(TOPOLOGY_FOLDER) --output $(RESULTS_PATH);  \