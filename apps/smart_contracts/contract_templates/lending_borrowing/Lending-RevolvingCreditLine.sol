// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RevolvingCreditLine {
    struct CreditLine {
        address borrower;
        uint256 creditLimit;
        uint256 currentDebt;
        uint256 interestRate;
        uint256 dueDate;
        bool active;
    }

    mapping(address => CreditLine) public creditLines;

    event CreditLineApproved(address indexed borrower, uint256 creditLimit);
    event FundsBorrowed(address indexed borrower, uint256 amount);
    event FundsRepaid(address indexed borrower, uint256 amount);

    function approveCreditLine(address borrower, uint256 creditLimit, uint256 interestRate) public {
        creditLines[borrower] = CreditLine({
            borrower: borrower,
            creditLimit: creditLimit,
            currentDebt: 0,
            interestRate: interestRate,
            dueDate: block.timestamp + 365 days,
            active: true
        });

        emit CreditLineApproved(borrower, creditLimit);
    }

    function borrowFunds(uint256 amount) public {
        CreditLine storage creditLine = creditLines[msg.sender];
        require(creditLine.active, "Credit line is not active");
        require(creditLine.currentDebt + amount <= creditLine.creditLimit, "Exceeds credit limit");

        creditLine.currentDebt += amount;
        payable(msg.sender).transfer(amount);

        emit FundsBorrowed(msg.sender, amount);
    }

    function repayFunds(uint256 amount) public {
        CreditLine storage creditLine = creditLines[msg.sender];
        require(creditLine.currentDebt >= amount, "Cannot repay more than debt");

        creditLine.currentDebt -= amount;
        payable(msg.sender).transfer(amount);

        emit FundsRepaid(msg.sender, amount);
    }

    function getCreditLineDetails(address borrower) public view returns (uint256 creditLimit, uint256 currentDebt, uint256 interestRate) {
        CreditLine memory creditLine = creditLines[borrower];
        return (creditLine.creditLimit, creditLine.currentDebt, creditLine.interestRate);
    }
}
