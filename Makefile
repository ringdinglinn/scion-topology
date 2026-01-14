# ==== CONFIG ====
ISDS := 1 2 3 4
AS_RANGE := 1 2 3 4 5
VERSION := 1.0

DEBIAN_DOCKER_DIR = $(CURDIR)

.PHONY: all build build-debian-base build-base build-scion up down purge

# ==== PATTERN RULES ====

all: up

build-debian-base:
	docker build -t debian-systemd:$(VERSION) \
		-f $(DEBIAN_DOCKER_DIR)/Dockerfile \
		$(DEBIAN_DOCKER_DIR)

build-base: build-debian-base
	docker build -t scion-base:$(VERSION) \
		-f ./base/Dockerfile \
		./base

# Pattern rule for scion nodes, e.g. scion32 -> isd3, as2
build-scion%:
	@isd=$(shell echo $* | cut -c1); \
	 as=$(shell echo $* | cut -c2); \
	 docker build -t scion$$isd$$as:$(VERSION) \
		-f ./ISD$$isd/scion$$isd$$as/Dockerfile \
		./ISD$$isd/scion$$isd$$as

# Pattern for building a whole AS group - ISD (e.g. build-isd1)
# Would need rework if AS # > 9
build-isd%:
	@isd=$*; \
	for as in $(AS_RANGE); do \
		$(MAKE) build-scion$$isd$$as; \
	done

build-monitor:
	docker build -t monitor:$(VERSION) \
		-f ./monitor/Dockerfile \
		./monitor

# Main build target
# First build base, then build monitor, then each scion-as
build: build-base build-monitor \
       $(foreach i,$(ISDS),$(foreach a,$(AS_RANGE),build-scion$(i)$(a)))

OS := $(shell uname)
up: install-bats build
ifeq ($(OS), Linux)
	docker compose up -d
else
	docker compose -f docker-compose.yml -f docker-compose.mac.yml up -d
endif
	bats test/

# Maybe include a pattern to start all existing containers

#install bats shell testing framework
install-bats:
	echo "Cloning bats-core repository..."
	git clone https://github.com/bats-core/bats-core.git
	echo "Installing bats..."
	cd bats-core && sudo ./install.sh /usr/local
	rm -rf bats-core
	echo "Checking bats installation..."
	if command -v bats >/dev/null 2>&1; then \
		echo "Bats installed successfully at $$(command -v bats)"; \
		bats --version; \
	else \
		echo "Bats installation failed or bats is not on your PATH."; \
		exit 1; \
	fi

#run test scripts


down:
	docker compose down

purge: down
	docker ps -aq --filter "name=scion" | xargs -r docker rm -f
	docker network ls -q --filter "name=^as_net_" --filter "name=^transit_net" | xargs -r docker network rm
