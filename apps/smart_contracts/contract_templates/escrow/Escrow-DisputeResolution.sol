// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DisputeResolutionEscrow {
    address public depositor;
    address public beneficiary;
    address public arbiter;
    address public mediator;
    bool public inDispute;

    constructor(address _beneficiary, address _arbiter, address _mediator) payable {
        depositor = msg.sender;
        beneficiary = _beneficiary;
        arbiter = _arbiter;
        mediator = _mediator;
    }

    function initiateDispute() external {
        require(msg.sender == depositor || msg.sender == beneficiary, "Only depositor or beneficiary can initiate");
        inDispute = true;
    }

    function resolveDispute(bool releaseFunds) external {
        require(msg.sender == mediator, "Only mediator can resolve disputes");
        require(inDispute, "No dispute to resolve");

        if (releaseFunds) {
            payable(beneficiary).transfer(address(this).balance);
        } else {
            payable(depositor).transfer(address(this).balance);
        }

        inDispute = false;
    }

    function releaseFunds() external {
        require(!inDispute, "Dispute is active");
        require(msg.sender == arbiter, "Only arbiter can release funds");

        payable(beneficiary).transfer(address(this).balance);
    }
}
