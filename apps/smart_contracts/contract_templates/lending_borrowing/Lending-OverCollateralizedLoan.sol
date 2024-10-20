// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract OvercollateralizedLoan {
    IERC20 public collateralToken;
    IERC20 public loanToken;

    struct Loan {
        address borrower;
        uint256 collateralAmount;
        uint256 loanAmount;
        uint256 interestRate;
        uint256 loanDueDate;
        bool repaid;
    }

    mapping(address => Loan) public loans;
    uint256 public collateralizationRatio;

    event LoanTaken(address indexed borrower, uint256 loanAmount, uint256 collateralAmount, uint256 interestRate, uint256 loanDueDate);
    event LoanRepaid(address indexed borrower, uint256 loanAmount);
    event LoanLiquidated(address indexed borrower, uint256 collateralAmount);

    constructor(IERC20 _collateralToken, IERC20 _loanToken, uint256 _collateralizationRatio) {
        collateralToken = _collateralToken;
        loanToken = _loanToken;
        collateralizationRatio = _collateralizationRatio;  // E.g., 150% (1.5x)
    }

    function takeLoan(uint256 collateralAmount, uint256 loanAmount, uint256 interestRate, uint256 duration) public {
        require(collateralAmount >= loanAmount * collateralizationRatio / 100, "Insufficient collateral");

        collateralToken.transferFrom(msg.sender, address(this), collateralAmount);
        loanToken.transfer(msg.sender, loanAmount);

        loans[msg.sender] = Loan({
            borrower: msg.sender,
            collateralAmount: collateralAmount,
            loanAmount: loanAmount,
            interestRate: interestRate,
            loanDueDate: block.timestamp + duration,
            repaid: false
        });

        emit LoanTaken(msg.sender, loanAmount, collateralAmount, interestRate, block.timestamp + duration);
    }

    function repayLoan() public {
        Loan storage loan = loans[msg.sender];
        require(!loan.repaid, "Loan already repaid");
        require(block.timestamp <= loan.loanDueDate, "Loan is overdue");

        uint256 repaymentAmount = loan.loanAmount + (loan.loanAmount * loan.interestRate) / 100;
        loanToken.transferFrom(msg.sender, address(this), repaymentAmount);
        collateralToken.transfer(msg.sender, loan.collateralAmount);

        loan.repaid = true;
        emit LoanRepaid(msg.sender, loan.loanAmount);
    }

    function liquidateLoan(address borrower) public {
        Loan storage loan = loans[borrower];
        require(block.timestamp > loan.loanDueDate, "Loan is not overdue");
        require(!loan.repaid, "Loan already repaid");

        // Liquidate collateral
        collateralToken.transfer(msg.sender, loan.collateralAmount);
        delete loans[borrower];

        emit LoanLiquidated(borrower, loan.collateralAmount);
    }
}
