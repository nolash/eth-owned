pragma solidity >= 0.6.11;

contract Owned {

	// EIP173
	address public owner;

	address newOwner;

	// EIP173
	event OwnershipTransferred(address indexed _previousOwner, address indexed _newOwner);

	constructor() public {
		owner = msg.sender;
	}

	// EIP173
	function transferOwnership(address _newOwner) public returns (bool) {
		require(owner == msg.sender);
		newOwner = _newOwner;
	}

	function acceptOwnership() public returns (bool) {
		address oldOwner;

		require(newOwner == msg.sender);
		oldOwner = owner;
		owner = newOwner;
		emit OwnershipTransferred(oldOwner, owner);
		return true;
	}
}
