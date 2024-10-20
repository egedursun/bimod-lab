// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PriceOracle {
    address public admin;
    mapping(address => bool) public trustedSources;
    mapping(address => uint256) public latestPrices;

    event PriceUpdated(address indexed source, uint256 price);

    constructor() {
        admin = msg.sender;
    }

    function addTrustedSource(address source) public {
        require(msg.sender == admin, "Only admin can add sources");
        trustedSources[source] = true;
    }

    function removeTrustedSource(address source) public {
        require(msg.sender == admin, "Only admin can remove sources");
        trustedSources[source] = false;
    }

    function updatePrice(uint256 price) public {
        require(trustedSources[msg.sender], "Not a trusted source");

        latestPrices[msg.sender] = price;
        emit PriceUpdated(msg.sender, price);
    }

    function getAveragePrice() public view returns (uint256) {
        uint256 totalPrice;
        uint256 sourceCount;

        for (uint256 i = 0; i < address(this).balance; i++) {
            if (trustedSources[msg.sender]) {
                totalPrice += latestPrices[msg.sender];
                sourceCount++;
            }
        }

        return totalPrice / sourceCount;
    }
}
