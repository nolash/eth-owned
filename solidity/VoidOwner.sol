pragma solidity >=0.6.11;

// SPDX-License-Identifier: GPL-3.0-or-later

contract VoidOwner {

	event OwnershipTaken(address _result);

	// Implements OwnedTaker
	function takeOwnership(address _contract) public returns (bool) {
		bool ok;
		bytes memory result;
		address newOwner;

		(ok, result) = _contract.call(abi.encodeWithSignature("acceptOwnership()"));
		require(ok, "ERR_ACCEPT");

		(ok, result) = _contract.call(abi.encodeWithSignature("owner()"));
		require(ok, "ERR_INTERFACE");
		newOwner = abi.decode(result, (address)); 
		require(address(this) == newOwner);
		
		emit OwnershipTaken(_contract);
		return ok;
	}

	// Implements EIP165
	function supportsInterface(bytes4 _sum) public pure returns (bool) {
		if (_sum == 0x6b578339) { // OwnedTaker
			return true;
		}
		if (_sum == 0x01ffc9a7) { // EIP165
			return true;
		}
		return false;
	}
}
