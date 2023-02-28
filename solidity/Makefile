SOLC = /usr/bin/solc

all:
	$(SOLC) VoidOwner.sol --abi --evm-version byzantium | awk 'NR>3' > VoidOwner.json
	$(SOLC) VoidOwner.sol --bin --evm-version byzantium | awk 'NR>3' > VoidOwner.bin
	truncate -s -1 VoidOwner.bin
	$(SOLC) Owned.sol --abi --evm-version byzantium | awk 'NR>3' > Owned.json
	$(SOLC) Owned.sol --bin --evm-version byzantium | awk 'NR>3' > Owned.bin
	truncate -s -1 Owned.bin
	$(SOLC) OwnedSimple.sol --abi --evm-version byzantium | awk 'NR>3' > OwnedSimple.json
	$(SOLC) OwnedSimple.sol --bin --evm-version byzantium | awk 'NR>3' > OwnedSimple.bin
	truncate -s -1 OwnedSimple.bin

test: all
	python ../python/tests/test_basic.py

install: all
	cp -v VoidOwner.json ../python/eth_owned/data/
	cp -v VoidOwner.bin ../python/eth_owned/data/
	cp -v Owned.json ../python/eth_owned/data/
	cp -v Owned.bin ../python/eth_owned/data/
	cp -v OwnedSimple.json ../python/eth_owned/data/
	cp -v OwnedSimple.bin ../python/eth_owned/data/
	
.PHONY: test install
