// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DynamicInterestLoan {
    uint256 public baseInterestRate;
    uint256 public loanDemand;
    uint256 public availableLiquidity;
    uint256 public lastUpdated;

    struct Loan {
        address borrower;
        uint256 amount;
        uint256 interestRate;
        uint256 dueDate;
        bool repaid;
    }

    mapping(address => Loan) public loans;

    event LoanTaken(address indexed borrower, uint256 amount, uint256 interestRate);
    event LoanRepaid(address indexed borrower, uint256 amount);

    constructor(uint256 _baseInterestRate, uint256 _initialLiquidity) {
        baseInterestRate = _baseInterestRate;
        availableLiquidity = _initialLiquidity;
        lastUpdated = block.timestamp;
    }

    function calculateInterestRate() public view returns (uint256) {
        return baseInterestRate + (loanDemand * 100) / availableLiquidity;
    }

    function takeLoan(uint256 amount, uint256 duration) public {
        require(availableLiquidity >= amount, "Insufficient liquidity");

        uint256 currentInterestRate = calculateInterestRate();
        loans[msg.sender] = Loan({
            borrower: msg.sender,
            amount: amount,
            interestRate: currentInterestRate,
            dueDate: block.timestamp + duration,
            repaid: false
        });

        availableLiquidity -= amount;
        loanDemand += amount;

        emit LoanTaken(msg.sender, amount, currentInterestRate);
    }

    function repayLoan() public {
        Loan storage loan = loans[msg.sender];
        require(!loan.repaid, "Loan already repaid");
        require(block.timestamp <= loan.dueDate, "Loan is overdue");

        uint256 repaymentAmount = loan.amount + (loan.amount * loan.interestRate) / 100;
        payable(msg.sender).transfer(repaymentAmount);

        loan.repaid = true;
        availableLiquidity += loan.amount;
        loanDemand -= loan.amount;

        emit LoanRepaid(msg.sender, loan.amount);
    }
}
