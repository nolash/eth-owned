SOLC = /usr/bin/solc

all:
	$(SOLC) VoidOwner.sol --abi --evm-version byzantium | awk 'NR>3' > VoidOwner.json
	$(SOLC) VoidOwner.sol --bin --evm-version byzantium | awk 'NR>3' > VoidOwner.bin
	truncate -s -1 VoidOwner.bin
	$(SOLC) Owned.sol --abi --evm-version byzantium | awk 'NR>3' > Owned.json
	$(SOLC) Owned.sol --bin --evm-version byzantium | awk 'NR>3' > Owned.bin
	truncate -s -1 Owned.bin

test: all
	python ../python/tests/test_basic.py

install: all
	cp -v VoidOwner.{json,bin} ../python/eth_owned/data/
	cp -v Owned.{json,bin} ../python/eth_owned/data/
	
.PHONY: test install
