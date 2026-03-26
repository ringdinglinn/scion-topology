# ==== CONFIG ====
NETWORK_CONFIG := topology_optimization/topologies/topo7/topo7_it0.yaml
TOPOLOGY_FOLDER := topology_optimization/topologies
RESULTS := topology_optimization/results/results.csv
CONTAINER_TOPOLOGIES_PATH := tmp/container-topologies/
PLOTS_FOLDER := topology_optimization/plots/
SHOWPATHS_DATA := topology_optimization/data/show_paths
SHOWPATHS_RESULTS := topology_optimization/results/results_paths.csv

CONFIG_MK := .isd-vars.mk

.PHONY: $(CONFIG_MK)
$(CONFIG_MK):
	@python3 -m scripts.parse-isd-config $(NETWORK_CONFIG) > $(CONFIG_MK)

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
		--build-arg NETWORK_CONFIG=$(NETWORK_CONFIG) \
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
		--build-arg NETWORK_CONFIG=$(NETWORK_CONFIG) \
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
	python3 -m scripts.generate-compose \
		--config $(NETWORK_CONFIG) \
		--version $(VERSION)

generate-topologies:
	python3 -m scripts.generate-topologies \
		-tp $(NETWORK_CONFIG) \
		--output-dir $(CONTAINER_TOPOLOGIES_PATH)

generate-nodeconfig:
	python3 -m scripts.generate-nodeconfig --config $(NETWORK_CONFIG)

generate-tests:
	python3 -m scripts.generate-tests --config $(NETWORK_CONFIG)

generate-web-ui:
	python3 -m scripts.generate-web-ui \
		--config $(NETWORK_CONFIG) \
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

TOPO_OPTIM_FOLDERS := topo0

# topo-optim:
# 	@for topo in $(TOPO_OPTIM_FOLDERS); do \
# 		file=$$(ls topologies/$$topo/*_it0.yaml); \
# 		python3 -m scripts.rewiring.rewire_spectral -tc $$file; \
# 		python3 -m scripts.rewiring.rewire_np -tc $$file; \
# 	done

topo-optim:
	@for topo in $(TOPOLOGY_FOLDER)/*/; do \
		file=$$(ls $$topo*_it0.yaml) ; \
		python3 -m scripts.rewiring.rewire_spectral -tc $$file -o $$topo -k 5; \
		python3 -m scripts.rewiring.rewire_np -tc $$file -o $$topo -k 5; \
	done

topo-eval: 
	python3 -m scripts.rewiring.evaluate_topology -i $(TOPOLOGY_FOLDER) -o $(RESULTS); \

topo-plot:
	python3 -m scripts.rewiring.plot_topology \
	-i $(RESULTS) \
	-g "^([^_]+)" \
	-sg "_([^_]+)_" \
	-m "cheeger_constant" "spectral_gap" "algebraic_connectivity" \
	-s topology \
	-o $(PLOTS_FOLDER) \
	-t $(TOPOLOGY_FOLDER) \
	--border-breadth \
	--graphs

run-path-evaluation:
	@for topo in $(TOPOLOGY_FOLDER)/topo*/; do \
		it0=$$(ls $$topo*_it0.yaml); \
		$(MAKE) rebuild NETWORK_CONFIG=$$it0; \
		for file in $$topo*_it*.yaml; do \
			$(MAKE) path-test NETWORK_CONFIG=$$file; \
		done; \
	done
	@$(MAKE) eval-paths
	@$(MAKE) plot-paths

path-test:
	@echo ">>> Running path evaluation for $(NETWORK_CONFIG)"; \
	retries=3; \
	until $(MAKE) up NETWORK_CONFIG=$(NETWORK_CONFIG); do \
		echo ">>> up failed, retrying ($$retries left)..."; \
		$(MAKE) down; \
		retries=$$((retries - 1)); \
		if [ $$retries -eq 0 ]; then \
			echo ">>> up failed after retries, skipping $(NETWORK_CONFIG)"; \
			$(MAKE) down; \
			exit 0; \
		fi; \
		sleep 5; \
	done; \
	sleep 30; \
	$(MAKE) show-paths NETWORK_CONFIG=$(NETWORK_CONFIG) SHOWPATHS_DATA=$(SHOWPATHS_DATA); \
	$(MAKE) down


show-paths:
	python3 -m scripts.rewiring.show_paths --config $(NETWORK_CONFIG) --output-path $(SHOWPATHS_DATA); \

eval-paths:
	python3 -m scripts.rewiring.evaluate_paths --folder $(SHOWPATHS_DATA) --topologies $(TOPOLOGY_FOLDER) --output $(SHOWPATHS_RESULTS);  \

plot-paths:
	python3 -m scripts.rewiring.plot_topology \
	-i $(SHOWPATHS_RESULTS) \
	-g "^([^_]+)" \
	-sg "_([^_]+)_" \
	-m "intra_isd_paths_scion+inter_isd_paths_scion" \
	-s topology \
	-o $(PLOTS_FOLDER) \
	-t $(TOPOLOGY_FOLDER)