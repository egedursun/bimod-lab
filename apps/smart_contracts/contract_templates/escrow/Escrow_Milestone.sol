// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MilestoneEscrow {
    address public depositor;
    address public beneficiary;
    address public arbiter;
    uint256 public milestoneCount;
    uint256 public currentMilestone;
    uint256 public amountPerMilestone;

    constructor(
        address _beneficiary,
        address _arbiter,
        uint256 _milestoneCount
    ) payable {
        require(_milestoneCount > 0, "Must have at least one milestone");

        depositor = msg.sender;
        beneficiary = _beneficiary;
        arbiter = _arbiter;
        milestoneCount = _milestoneCount;
        amountPerMilestone = msg.value / milestoneCount;
    }

    function approveMilestone() external {
        require(msg.sender == arbiter, "Only arbiter can approve");
        require(currentMilestone < milestoneCount, "All milestones completed");

        payable(beneficiary).transfer(amountPerMilestone);
        currentMilestone++;
    }

    function cancel() external {
        require(msg.sender == arbiter, "Only arbiter can cancel");
        require(currentMilestone < milestoneCount, "Cannot cancel after milestones completed");

        uint256 remainingAmount = address(this).balance;
        payable(depositor).transfer(remainingAmount);
    }
}
