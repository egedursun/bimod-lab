// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract DecentralizedExchange {
    IERC20 public tokenA;
    IERC20 public tokenB;

    uint256 public reserveA;
    uint256 public reserveB;

    event TokenSwapped(address indexed user, uint256 amountA, uint256 amountB);

    constructor(IERC20 _tokenA, IERC20 _tokenB) {
        tokenA = _tokenA;
        tokenB = _tokenB;
    }

    function provideLiquidity(uint256 amountA, uint256 amountB) public {
        require(amountA > 0 && amountB > 0, "Invalid liquidity amounts");

        tokenA.transferFrom(msg.sender, address(this), amountA);
        tokenB.transferFrom(msg.sender, address(this), amountB);

        reserveA += amountA;
        reserveB += amountB;
    }

    function swapTokens(uint256 amountIn, bool isTokenAForB) public {
        require(amountIn > 0, "Invalid swap amount");

        uint256 amountOut;

        if (isTokenAForB) {
            require(reserveA >= amountIn, "Insufficient token A liquidity");
            amountOut = (amountIn * reserveB) / reserveA;
            tokenA.transferFrom(msg.sender, address(this), amountIn);
            tokenB.transfer(msg.sender, amountOut);
            reserveA += amountIn;
            reserveB -= amountOut;
        } else {
            require(reserveB >= amountIn, "Insufficient token B liquidity");
            amountOut = (amountIn * reserveA) / reserveB;
            tokenB.transferFrom(msg.sender, address(this), amountIn);
            tokenA.transfer(msg.sender, amountOut);
            reserveB += amountIn;
            reserveA -= amountOut;
        }

        emit TokenSwapped(msg.sender, amountIn, amountOut);
    }
}
