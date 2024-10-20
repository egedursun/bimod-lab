// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RecurringPaymentsEscrow {
    address public depositor;
    address public beneficiary;
    uint256 public interval;  // Interval in seconds
    uint256 public lastPaymentTime;
    uint256 public paymentAmount;

    constructor(address _beneficiary, uint256 _interval, uint256 _paymentAmount) payable {
        depositor = msg.sender;
        beneficiary = _beneficiary;
        interval = _interval;
        paymentAmount = _paymentAmount;
        lastPaymentTime = block.timestamp;
    }

    function releaseFunds() public {
        require(block.timestamp >= lastPaymentTime + interval, "Next payment not yet due");

        lastPaymentTime = block.timestamp;
        payable(beneficiary).transfer(paymentAmount);
    }

    function depositFunds() external payable {
        require(msg.sender == depositor, "Only depositor can deposit funds");
    }

    function cancel() external {
        require(msg.sender == depositor, "Only depositor can cancel");

        payable(depositor).transfer(address(this).balance);
    }
}
