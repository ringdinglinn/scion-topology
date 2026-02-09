# ==== CONFIG ====
ISDS := 1 2 3 4
AS_RANGE := 1 2 3 4 5
VERSION := 1.0

DEBIAN_DOCKER_DIR = $(CURDIR)

.PHONY: all build rebuild build-debian-base build-base \
        build-scion rebuild-scion rebuild-base rebuild-monitor \
        up down purge

# ==== PATTERN RULES ====

all: up

build-debian-base:
	cd "$(DEBIAN_DOCKER_DIR)" && docker build -t debian-systemd:$(VERSION) .

build-base: build-debian-base
	docker build -t scion-base:$(VERSION) \
		--build-arg ISDS="$(ISDS)" \
		--build-arg AS_COUNT=$(words $(AS_RANGE)) \
		-f ./base/Dockerfile \
		./base

# Pattern rule for scion nodes, e.g. scion32 -> isd3, as2
build-scion:
	@counter=1; \
	for isd in $(ISDS); do \
		for as in $(AS_RANGE); do \
			echo ">>> Building SCION node ISD=$$isd AS=$$as INDEX=$$counter"; \
			docker build --progress=plain \
				-t scion$$isd$$as:$(VERSION) \
				--build-arg INDEX=$$counter \
				-f ./template/Dockerfile \
				./topologies || exit 1; \
			counter=$$((counter+1)); \
		done; \
	done

# Pattern for endhost
build-endhost%:
	@as=$*; \
	docker build -t endhost-as$$as:$(VERSION) \
		-f ./endhosts/endhost-as$$as/Dockerfile \
		./endhosts/endhost-as$$as

# Build the specific endhost
build-all-endhost: build-endhost15 build-endhost35


build-monitor:
	docker build -t monitor:$(VERSION) \
		-f ./monitor/Dockerfile \
		./monitor

# Main build target
# First build base, then build monitor, then each scion-as
build: generate-compose build-base build-monitor \
       build-scion \
	   build-all-endhost

# Rebuild targets (force no-cache)
rebuild: generate-compose rebuild-base rebuild-monitor \
         rebuild-scion

rebuild-base:
	docker build --no-cache -t debian-systemd:$(VERSION) .
	docker build --no-cache -t scion-base:$(VERSION) \
		--build-arg ISDS="$(ISDS)" \
		--build-arg ASES="$(AS_RANGE)" \
		-f ./base/Dockerfile \
		./base

rebuild-scion:
	@counter=1; \
	for isd in $(ISDS); do \
		for as in $(AS_RANGE); do \
			echo ">>> Building SCION node ISD=$$isd AS=$$as INDEX=$$counter"; \
			docker build --no-cache --progress=plain \
				-t scion$$isd$$as:$(VERSION) \
				--build-arg INDEX=$$counter \
				-f ./template/Dockerfile \
				./topologies || exit 1; \
			counter=$$((counter+1)); \
		done; \
	done

rebuild-monitor:
	docker build --no-cache -t monitor:$(VERSION) \
		-f ./monitor/Dockerfile \
		./monitor

generate-compose:
	python3 scripts/generate-compose.py \
		--isds "$(ISDS)" \
		--as-range "$(AS_RANGE)" \
		--version $(VERSION) 

OS := $(shell uname)
up: build
ifeq ($(OS), Linux)
	docker compose up -d
else
	docker compose -f docker-compose.yml -f docker-compose.mac.yml up -d
endif

# Maybe include a pattern to start all existing containers

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


down:
	docker compose down

purge: down
	docker ps -aq --filter "name=scion" | xargs -r docker rm -f
	docker network ls -q --filter "name=^as_net_" --filter "name=^transit_net" | xargs -r docker network rm


.PHONY: test

test: install-bats
	bats test/