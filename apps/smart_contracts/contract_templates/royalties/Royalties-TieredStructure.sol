// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TieredRoyalties {
    address public creator;
    uint256 public totalSales;
    mapping(uint256 => uint256) public royaltyTiers;  // Maps sales thresholds to royalty percentages

    event RoyaltyPaid(address indexed recipient, uint256 amount, uint256 totalSales);

    constructor() {
        creator = msg.sender;

        // Example: Setting tiers for different sales thresholds
        royaltyTiers[100 ether] = 5;  // 5% royalties for sales under 100 ether
        royaltyTiers[200 ether] = 10; // 10% royalties for sales between 100 and 200 ether
        royaltyTiers[500 ether] = 15; // 15% royalties for sales over 500 ether
    }

    function payRoyalty(uint256 saleAmount) public payable {
        require(msg.value == saleAmount, "Incorrect sale amount");

        uint256 royaltyRate = getRoyaltyRate();
        uint256 royaltyAmount = (saleAmount * royaltyRate) / 100;

        payable(creator).transfer(royaltyAmount);
        totalSales += saleAmount;

        emit RoyaltyPaid(creator, royaltyAmount, totalSales);
    }

    function getRoyaltyRate() public view returns (uint256) {
        if (totalSales >= 500 ether) {
            return royaltyTiers[500 ether];
        } else if (totalSales >= 200 ether) {
            return royaltyTiers[200 ether];
        } else {
            return royaltyTiers[100 ether];
        }
    }
}
