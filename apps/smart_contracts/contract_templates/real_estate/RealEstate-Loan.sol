// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RealEstateLoan {
    address public lender;
    address public borrower;
    uint256 public loanAmount;
    uint256 public collateralValue;
    uint256 public interestRate;
    uint256 public loanDueDate;
    bool public loanRepaid;
    bool public loanSeized;

    event LoanTaken(address indexed borrower, uint256 loanAmount, uint256 collateralValue, uint256 interestRate);
    event LoanRepaid(address indexed borrower);
    event CollateralSeized(address indexed lender, uint256 collateralValue);

    constructor(
        address _borrower,
        uint256 _loanAmount,
        uint256 _collateralValue,
        uint256 _interestRate,
        uint256 _duration
    ) {
        lender = msg.sender;
        borrower = _borrower;
        loanAmount = _loanAmount;
        collateralValue = _collateralValue;
        interestRate = _interestRate;
        loanDueDate = block.timestamp + _duration;
        loanRepaid = false;
        loanSeized = false;
    }

    function takeLoan() public {
        require(msg.sender == borrower, "Only the borrower can take the loan");
        require(!loanRepaid, "Loan has already been repaid");

        payable(borrower).transfer(loanAmount);
        emit LoanTaken(borrower, loanAmount, collateralValue, interestRate);
    }

    function repayLoan() public payable {
        require(msg.sender == borrower, "Only the borrower can repay the loan");
        require(msg.value == loanAmount + (loanAmount * interestRate) / 100, "Incorrect repayment amount");

        loanRepaid = true;
        emit LoanRepaid(borrower);
    }

    function seizeCollateral() public {
        require(block.timestamp > loanDueDate, "Loan is not yet due");
        require(!loanRepaid, "Loan has already been repaid");

        loanSeized = true;
        // Transfer property (collateral) to the lender
        emit CollateralSeized(lender, collateralValue);
    }
}
