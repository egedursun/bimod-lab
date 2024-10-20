// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PercentageRoyalties {
    address public creator;
    mapping(address => uint256) public royaltyRecipients;
    uint256 public totalRoyaltyPercentage;

    event RoyaltyDistributed(address indexed recipient, uint256 amount);

    constructor(address[] memory recipients, uint256[] memory percentages) {
        require(recipients.length == percentages.length, "Mismatched recipients and percentages");

        creator = msg.sender;

        for (uint256 i = 0; i < recipients.length; i++) {
            royaltyRecipients[recipients[i]] = percentages[i];
            totalRoyaltyPercentage += percentages[i];
        }

        require(totalRoyaltyPercentage <= 100, "Total percentages exceed 100");
    }

    function distributeRoyalties() public payable {
        require(msg.value > 0, "No funds to distribute");

        for (uint256 i = 0; i < royaltyRecipients.length; i++) {
            uint256 amount = (msg.value * royaltyRecipients[recipients[i]]) / 100;
            payable(recipients[i]).transfer(amount);

            emit RoyaltyDistributed(recipients[i], amount);
        }
    }
}
