// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract ImpermanentLossProtectionPool {
    IERC20 public tokenA;
    IERC20 public tokenB;
    IERC20 public insuranceFund;

    uint256 public totalLiquidityA;
    uint256 public totalLiquidityB;
    mapping(address => uint256) public liquidityShares;
    mapping(address => uint256) public initialPrices;

    constructor(IERC20 _tokenA, IERC20 _tokenB, IERC20 _insuranceFund) {
        tokenA = _tokenA;
        tokenB = _tokenB;
        insuranceFund = _insuranceFund;
    }

    function provideLiquidity(uint256 amountA, uint256 amountB, uint256 priceA, uint256 priceB) public {
        require(amountA > 0 && amountB > 0, "Amounts must be greater than 0");

        tokenA.transferFrom(msg.sender, address(this), amountA);
        tokenB.transferFrom(msg.sender, address(this), amountB);

        uint256 liquidity = _calculateLiquidity(amountA, amountB);
        liquidityShares[msg.sender] += liquidity;
        initialPrices[msg.sender] = _averagePrice(priceA, priceB);

        totalLiquidityA += amountA;
        totalLiquidityB += amountB;
    }

    function removeLiquidity(uint256 liquidity, uint256 currentPriceA, uint256 currentPriceB) public {
        require(liquidityShares[msg.sender] >= liquidity, "Insufficient liquidity");

        uint256 amountA = (liquidity * totalLiquidityA) / _totalLiquidity();
        uint256 amountB = (liquidity * totalLiquidityB) / _totalLiquidity();
        uint256 initialPrice = initialPrices[msg.sender];
        uint256 currentPrice = _averagePrice(currentPriceA, currentPriceB);

        uint256 impermanentLoss = _calculateImpermanentLoss(initialPrice, currentPrice);

        if (impermanentLoss > 0) {
            insuranceFund.transfer(msg.sender, impermanentLoss);
        }

        liquidityShares[msg.sender] -= liquidity;

        tokenA.transfer(msg.sender, amountA);
        tokenB.transfer(msg.sender, amountB);

        totalLiquidityA -= amountA;
        totalLiquidityB -= amountB;
    }

    function _calculateLiquidity(uint256 amountA, uint256 amountB) internal pure returns (uint256) {
        return amountA + amountB; // Simplified liquidity calculation
    }

    function _totalLiquidity() internal view returns (uint256) {
        return totalLiquidityA + totalLiquidityB;
    }

    function _averagePrice(uint256 priceA, uint256 priceB) internal pure returns (uint256) {
        return (priceA + priceB) / 2;
    }

    function _calculateImpermanentLoss(uint256 initialPrice, uint256 currentPrice) internal pure returns (uint256) {
        if (currentPrice < initialPrice) {
            return (initialPrice - currentPrice) * 100 / initialPrice;  // Percentage loss
        }
        return 0;
    }
}
