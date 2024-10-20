// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PerformanceRoyalties {
    address public creator;
    uint256 public salesMilestone;
    uint256 public royaltiesPaid;

    event MilestoneAchieved(address indexed creator, uint256 royaltiesPaid);

    constructor(uint256 _salesMilestone) {
        creator = msg.sender;
        salesMilestone = _salesMilestone;
    }

    function payPerformanceRoyalty(uint256 saleAmount) public payable {
        require(msg.value == saleAmount, "Incorrect payment amount");

        royaltiesPaid += msg.value;

        if (royaltiesPaid >= salesMilestone) {
            releaseRoyalties();
        }
    }

    function releaseRoyalties() internal {
        payable(creator).transfer(royaltiesPaid);
        emit MilestoneAchieved(creator, royaltiesPaid);

        royaltiesPaid = 0;  // Reset for the next milestone
    }
}
