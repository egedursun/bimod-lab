// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RefundEscrow {
    address public depositor;
    address public beneficiary;
    address public arbiter;
    bool public isRefundRequested;
    uint256 public refundRequestTime;

    constructor(address _beneficiary, address _arbiter) payable {
        depositor = msg.sender;
        beneficiary = _beneficiary;
        arbiter = _arbiter;
    }

    function requestRefund() public {
        require(msg.sender == depositor, "Only depositor can request refund");
        require(!isRefundRequested, "Refund already requested");

        isRefundRequested = true;
        refundRequestTime = block.timestamp;
    }

    function approveRefund() public {
        require(msg.sender == arbiter, "Only arbiter can approve refund");
        require(isRefundRequested, "No refund requested");

        payable(depositor).transfer(address(this).balance);
    }

    function releaseFunds() public {
        require(msg.sender == arbiter, "Only arbiter can release funds");
        require(!isRefundRequested, "Refund is requested");

        payable(beneficiary).transfer(address(this).balance);
    }
}
