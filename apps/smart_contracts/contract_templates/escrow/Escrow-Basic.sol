// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleEscrow {
    address public depositor;
    address public beneficiary;
    address public arbiter;
    bool public isApproved;

    constructor(address _beneficiary, address _arbiter) payable {
        depositor = msg.sender;
        beneficiary = _beneficiary;
        arbiter = _arbiter;
    }

    function approve() external {
        require(msg.sender == arbiter, "Only arbiter can approve");
        require(!isApproved, "Already approved");

        isApproved = true;
        payable(beneficiary).transfer(address(this).balance);
    }

    function cancel() external {
        require(msg.sender == arbiter, "Only arbiter can cancel");
        require(!isApproved, "Cannot cancel after approval");

        payable(depositor).transfer(address(this).balance);
    }
}
