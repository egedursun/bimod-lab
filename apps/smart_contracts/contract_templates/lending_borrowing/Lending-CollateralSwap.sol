// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract CollateralSwap {
    IERC20 public loanToken;

    struct Loan {
        address borrower;
        IERC20 collateralToken;
        uint256 collateralAmount;
        uint256 loanAmount;
        uint256 interestRate;
        uint256 dueDate;
        bool repaid;
    }

    mapping(address => Loan) public loans;

    event LoanTaken(address indexed borrower, uint256 loanAmount, address collateralToken, uint256 collateralAmount);
    event CollateralSwapped(address indexed borrower, address oldCollateralToken, address newCollateralToken, uint256 newCollateralAmount);

    constructor(IERC20 _loanToken) {
        loanToken = _loanToken;
    }

    function takeLoan(IERC20 collateralToken, uint256 collateralAmount, uint256 loanAmount, uint256 interestRate, uint256 duration) public {
        require(collateralAmount > 0 && loanAmount > 0, "Amounts must be greater than 0");

        collateralToken.transferFrom(msg.sender, address(this), collateralAmount);
        loanToken.transfer(msg.sender, loanAmount);

        loans[msg.sender] = Loan({
            borrower: msg.sender,
            collateralToken: collateralToken,
            collateralAmount: collateralAmount,
            loanAmount: loanAmount,
            interestRate: interestRate,
            dueDate: block.timestamp + duration,
            repaid: false
        });

        emit LoanTaken(msg.sender, loanAmount, address(collateralToken), collateralAmount);
    }

    function swapCollateral(IERC20 newCollateralToken, uint256 newCollateralAmount) public {
        Loan storage loan = loans[msg.sender];
        require(!loan.repaid, "Loan already repaid");
        require(newCollateralAmount > 0, "New collateral amount must be greater than 0");

        // Return old collateral to borrower
        loan.collateralToken.transfer(msg.sender, loan.collateralAmount);

        // Accept new collateral
        newCollateralToken.transferFrom(msg.sender, address(this), newCollateralAmount);

        emit CollateralSwapped(msg.sender, address(loan.collateralToken), address(newCollateralToken), newCollateralAmount);

        // Update loan with new collateral
        loan.collateralToken = newCollateralToken;
        loan.collateralAmount = newCollateralAmount;
    }
}
