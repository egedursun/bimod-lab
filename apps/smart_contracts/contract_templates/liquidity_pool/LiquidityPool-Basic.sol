// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract BasicLiquidityPool {
    IERC20 public tokenA;
    IERC20 public tokenB;

    uint256 public totalLiquidityA;
    uint256 public totalLiquidityB;
    mapping(address => uint256) public liquidityShares;

    constructor(IERC20 _tokenA, IERC20 _tokenB) {
        tokenA = _tokenA;
        tokenB = _tokenB;
    }

    function provideLiquidity(uint256 amountA, uint256 amountB) public {
        require(amountA > 0 && amountB > 0, "Amounts must be greater than 0");

        tokenA.transferFrom(msg.sender, address(this), amountA);
        tokenB.transferFrom(msg.sender, address(this), amountB);

        uint256 liquidity = _calculateLiquidity(amountA, amountB);
        liquidityShares[msg.sender] += liquidity;

        totalLiquidityA += amountA;
        totalLiquidityB += amountB;
    }

    function removeLiquidity(uint256 liquidity) public {
        require(liquidityShares[msg.sender] >= liquidity, "Insufficient liquidity");

        uint256 amountA = (liquidity * totalLiquidityA) / _totalLiquidity();
        uint256 amountB = (liquidity * totalLiquidityB) / _totalLiquidity();

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
}
