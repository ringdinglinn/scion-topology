# ==== CONFIG ====
CONFIG_PATH := configurations/topo1/topo1_it.yaml
CONFIG_FOLDER := configurations
RESULTS_PATH := configurations/results/results.csv
TOPOLOGIES_PATH := topologies
PLOTS_FOLDER := configurations/plots/
SHOWPATHS_PATH := configurations/results/show_paths

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
		--build-arg CONFIG_PATH=$(CONFIG_PATH) \
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
		--build-arg CONFIG_PATH=$(CONFIG_PATH) \
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
		--config $(CONFIG_PATH) \
		--version $(VERSION)

generate-topologies:
	python3 scripts/generate-topologies.py \
		-tp $(CONFIG_PATH) \
		--output-dir $(TOPOLOGIES_PATH)

generate-nodeconfig:
	python3 scripts/generate-nodeconfig.py --config $(CONFIG_PATH)

generate-tests:
	python3 scripts/generate-tests.py --config $(CONFIG_PATH)

generate-web-ui:
	python3 scripts/generate-web-ui.py \
		--config $(CONFIG_PATH) \
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

# topo-optim: $(CONFIG_FOLDER)/*
# 	for topo in $^ ; do \
# 		file=$$(ls $$topo/*_it0.yaml) ; \
# 		python3 scripts/network-partition-scipy.py -tc $$file; \
# 	done

TOPO_OPTIM_FOLDER := configurations/topo2

topo-optim:
	file=$$(ls $(TOPO_OPTIM_FOLDER)/*_it0.yaml) ; \
	python3 scripts/network-partition-scipy.py -tc $$file

topo-eval: 
	python3 scripts/evaluate_topology.py -i $(CONFIG_FOLDER) -o $(RESULTS_PATH); \

topo-plot:
	python3 scripts/plot_topology.py \
	-i $(RESULTS_PATH) \
	-g "^([^_]+)" \
	-m "cheeger_constant" "spectral_gap" "algebraic_connectivity" "cheeger_raw" "num_scion_paths" "num_simple_paths" \
	-s topology \
	-o $(PLOTS_FOLDER) \
	-t $(CONFIG_FOLDER)

show-paths:
	python3 scripts/show_paths.py --config $(CONFIG_PATH) --output-path $(SHOWPATHS_PATH); \

eval-paths:
	python3 scripts/evaluate_paths.py --folder $(SHOWPATHS_PATH) --topologies $(CONFIG_FOLDER) --output $(RESULTS_PATH);  \