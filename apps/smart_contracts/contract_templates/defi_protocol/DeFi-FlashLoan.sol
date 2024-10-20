// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract FlashLoanProtocol {
    IERC20 public token;
    uint256 public fee;  // Fee percentage (e.g., 0.09%)

    event FlashLoanExecuted(address indexed borrower, uint256 amount, uint256 fee);

    constructor(IERC20 _token, uint256 _fee) {
        token = _token;
        fee = _fee;
    }

    function executeFlashLoan(uint256 amount, address borrower, bytes calldata data) public {
        require(amount <= token.balanceOf(address(this)), "Insufficient liquidity");

        uint256 loanFee = (amount * fee) / 100;
        uint256 totalRepayment = amount + loanFee;

        // Transfer loan amount to borrower
        token.transfer(borrower, amount);

        // Execute borrower function call
        (bool success, ) = borrower.call(data);
        require(success, "Flash loan execution failed");

        // Ensure the loan and fee are repaid
        token.transferFrom(borrower, address(this), totalRepayment);

        emit FlashLoanExecuted(borrower, amount, loanFee);
    }
}
