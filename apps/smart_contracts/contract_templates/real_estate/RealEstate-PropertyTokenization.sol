// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract PropertyToken is ERC20 {
    address public propertyOwner;
    string public propertyDetails;

    constructor(
        string memory _name,
        string memory _symbol,
        string memory _propertyDetails,
        uint256 _totalSupply
    ) ERC20(_name, _symbol) {
        propertyOwner = msg.sender;
        propertyDetails = _propertyDetails;
        _mint(msg.sender, _totalSupply);
    }

    function getPropertyDetails() public view returns (string memory) {
        return propertyDetails;
    }

    function transferOwnership(address newOwner) public {
        require(msg.sender == propertyOwner, "Only the property owner can transfer ownership");
        propertyOwner = newOwner;
    }
}
