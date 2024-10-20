// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ProgressiveEscrow {
    address public depositor;
    address public beneficiary;
    address public arbiter;
    uint256 public totalFunds;
    uint256 public releasedFunds;

    constructor(address _beneficiary, address _arbiter) payable {
        depositor = msg.sender;
        beneficiary = _beneficiary;
        arbiter = _arbiter;
        totalFunds = msg.value;
    }

    function releasePartialFunds(uint256 amount) public {
        require(msg.sender == arbiter, "Only arbiter can release funds");
        require(amount <= totalFunds - releasedFunds, "Cannot release more than available funds");

        releasedFunds += amount;
        payable(beneficiary).transfer(amount);
    }

    function releaseAllFunds() public {
        require(msg.sender == arbiter, "Only arbiter can release funds");
        uint256 remainingFunds = totalFunds - releasedFunds;
        payable(beneficiary).transfer(remainingFunds);
        releasedFunds = totalFunds;
    }

    function cancel() public {
        require(msg.sender == arbiter, "Only arbiter can cancel");

        payable(depositor).transfer(address(this).balance);
    }
}
