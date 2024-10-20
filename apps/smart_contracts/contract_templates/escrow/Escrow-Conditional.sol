// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ConditionalEscrow {
    address public depositor;
    address public beneficiary;
    address public arbiter;
    bool public conditionMet;

    constructor(address _beneficiary, address _arbiter) payable {
        depositor = msg.sender;
        beneficiary = _beneficiary;
        arbiter = _arbiter;
    }

    // Custom condition is checked here
    function setCondition(bool _conditionMet) external {
        require(msg.sender == arbiter, "Only arbiter can set the condition");
        conditionMet = _conditionMet;
    }

    function releaseFunds() external {
        require(conditionMet, "Condition has not been met");
        require(msg.sender == beneficiary, "Only beneficiary can release funds");

        payable(beneficiary).transfer(address(this).balance);
    }

    function cancel() external {
        require(msg.sender == arbiter, "Only arbiter can cancel");
        require(!conditionMet, "Cannot cancel after condition is met");

        payable(depositor).transfer(address(this).balance);
    }
}
