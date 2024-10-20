// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AutomatedPayment {
    struct Payment {
        address payer;
        address payee;
        uint256 amount;
        bool released;
    }

    mapping(uint256 => Payment) public payments;

    event PaymentScheduled(address indexed payer, address indexed payee, uint256 amount);
    event PaymentReleased(uint256 indexed paymentId, uint256 amount);

    function schedulePayment(address payee, uint256 amount) public {
        uint256 paymentId = uint256(keccak256(abi.encodePacked(msg.sender, payee, amount, block.timestamp)));

        payments[paymentId] = Payment({
            payer: msg.sender,
            payee: payee,
            amount: amount,
            released: false
        });

        emit PaymentScheduled(msg.sender, payee, amount);
    }

    function releasePayment(uint256 paymentId) public {
        Payment storage payment = payments[paymentId];
        require(!payment.released, "Payment already released");
        require(msg.sender == payment.payer, "Only the payer can release the payment");

        payment.released = true;
        payable(payment.payee).transfer(payment.amount);

        emit PaymentReleased(paymentId, payment.amount);
    }

    function getPaymentStatus(uint256 paymentId) public view returns (bool) {
        return payments[paymentId].released;
    }
}
