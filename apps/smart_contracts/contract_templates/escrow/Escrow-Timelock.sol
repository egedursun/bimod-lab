// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TimelockEscrow {
    address public depositor;
    address public beneficiary;
    address public arbiter;
    uint256 public releaseTime;

    constructor(address _beneficiary, address _arbiter, uint256 _releaseTime) payable {
        depositor = msg.sender;
        beneficiary = _beneficiary;
        arbiter = _arbiter;
        releaseTime = _releaseTime;
    }

    function releaseFunds() external {
        require(block.timestamp >= releaseTime, "Funds are locked");
        require(msg.sender == beneficiary, "Only the beneficiary can release");

        payable(beneficiary).transfer(address(this).balance);
    }

    function cancel() external {
        require(msg.sender == arbiter, "Only arbiter can cancel");
        require(block.timestamp < releaseTime, "Cannot cancel after release time");

        payable(depositor).transfer(address(this).balance);
    }
}
