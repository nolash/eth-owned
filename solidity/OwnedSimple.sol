pragma solidity >= 0.6.11;

// SPDX-License-Identifier: GPL-3.0-or-later

contract Owned {

	// EIP173
	address public owner;

	// EIP173
	event OwnershipTransferred(address indexed _previousOwner, address indexed _newOwner);

	constructor() public {
		owner = msg.sender;
	}

	// EIP173
	function transferOwnership(address _newOwner) public returns (bool) {
		require(owner == msg.sender);
		owner = _newOwner;
	}
}
