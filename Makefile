# ==== CONFIG ====
CONFIG_PATH := base/isds.yaml
CONFIG_VARS := $(shell python3 scripts/parse-isd-config.py $(CONFIG_PATH))
$(eval $(CONFIG_VARS))

VERSION := 1.0
DEBIAN_DOCKER_DIR = $(CURDIR)

.PHONY: all build rebuild build-debian-base build-base \
        build-scion rebuild-scion rebuild-base rebuild-monitor \
        up down purge show-config

# Debug target to see loaded config
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
		./base

# Pattern rule for scion nodes
build-scion%:
	@isd=$(shell echo $* | cut -c1); \
	 as=$(shell echo $* | cut -c2); \
	 docker build -t scion$$isd$$as:$(VERSION) \
		--build-arg ISD=$$isd \
		--build-arg AS=$$as \
		-f ./template/Dockerfile \
		./topologies

build-endhost%:
	@as=$*; \
	docker build -t endhost-as$$as:$(VERSION) \
		-f ./endhosts/endhost-as$$as/Dockerfile \
		./endhosts/endhost-as$$as

build-all-endhost: build-endhost15 build-endhost35

build-monitor:
	docker build -t monitor:$(VERSION) \
		-f ./monitor/Dockerfile \
		./monitor

# Main build target - dynamically generate targets per ISD
build: generate-compose build-base build-monitor \
       $(foreach i,$(ISDS),$(foreach a,$(ISD$(i)_AS_RANGE),build-scion$(i)$(a))) \
	   build-all-endhost

rebuild: generate-compose rebuild-base rebuild-monitor \
         $(foreach i,$(ISDS),$(foreach a,$(ISD$(i)_AS_RANGE),rebuild-scion$(i)$(a)))

rebuild-base:
	docker build --no-cache -t debian-systemd:$(VERSION) .
	docker build --no-cache -t scion-base:$(VERSION) \
		-f ./base/Dockerfile \
		./base

rebuild-scion%:
	@isd=$(shell echo $* | cut -c1); \
	 as=$(shell echo $* | cut -c2); \
	 docker build --no-cache -t scion$$isd$$as:$(VERSION) \
		--build-arg ISD=$$isd \
		--build-arg AS=$$as \
		-f ./template/Dockerfile \
		./topologies

rebuild-monitor:
	docker build --no-cache -t monitor:$(VERSION) \
		-f ./monitor/Dockerfile \
		./monitor

generate-compose:
	python3 scripts/generate-compose.py \
		--config $(CONFIG_PATH) \
		--version $(VERSION)

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