pragma solidity >= 0.6.11;

// SPDX-License-Identifier: GPL-3.0-or-later

contract Owned {

	// EIP173
	address public owner;

	address newOwner;

	uint8 finalOwner; 

	// EIP173
	event OwnershipTransferred(address indexed _previousOwner, address indexed _newOwner);

	constructor() public {
		owner = msg.sender;
	}

	// EIP173
	function transferOwnership(address _newOwner) public returns (bool) {
		require(owner == msg.sender);
		require(finalOwner < 2);
		newOwner = _newOwner;
	}

	function transferOwnershipFinal(address _newOwner) public returns (bool) {
		this.transferOwnership(_newOwner);
		finalOwner = 1;
	}

	function acceptOwnership() public returns (bool) {
		address oldOwner;

		require(newOwner == msg.sender);
		oldOwner = owner;
		owner = newOwner;
		emit OwnershipTransferred(oldOwner, owner);
		if (finalOwner == 1) {
			finalOwner = 2;
		}
		return true;
	}
}
