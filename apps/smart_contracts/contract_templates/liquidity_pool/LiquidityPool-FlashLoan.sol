// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract FlashLoanLiquidityPool {
    IERC20 public token;
    uint256 public totalLiquidity;
    uint256 public feePercentage;  // Fee charged on the loan (e.g., 0.09%)

    constructor(IERC20 _token, uint256 _feePercentage) {
        token = _token;
        feePercentage = _feePercentage;
    }

    function provideLiquidity(uint256 amount) public {
        require(amount > 0, "Cannot provide 0 liquidity");
        token.transferFrom(msg.sender, address(this), amount);
        totalLiquidity += amount;
    }

    function flashLoan(uint256 amount, address borrower, bytes calldata data) public {
        require(amount <= totalLiquidity, "Insufficient liquidity");

        uint256 fee = (amount * feePercentage) / 100;
        totalLiquidity -= amount;

        // Transfer loan amount to borrower
        token.transfer(borrower, amount);

        // Execute callback function in borrower contract
        (bool success,) = borrower.call(data);
        require(success, "Flash loan callback failed");

        // Ensure loan and fee are repaid
        uint256 totalRepayment = amount + fee;
        token.transferFrom(borrower, address(this), totalRepayment);

        totalLiquidity += totalRepayment;
    }
}
