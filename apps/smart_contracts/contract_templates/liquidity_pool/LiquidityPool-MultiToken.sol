// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract MultiTokenLiquidityPool {
    IERC20[] public tokens;
    uint256[] public totalLiquidity;
    mapping(address => uint256[]) public liquidityShares;

    constructor(IERC20[] memory _tokens) {
        tokens = _tokens;
        totalLiquidity = new uint256[](_tokens.length);
    }

    function provideLiquidity(uint256[] memory amounts) public {
        require(amounts.length == tokens.length, "Invalid token amounts");

        for (uint256 i = 0; i < tokens.length; i++) {
            require(amounts[i] > 0, "Amounts must be greater than 0");
            tokens[i].transferFrom(msg.sender, address(this), amounts[i]);
            totalLiquidity[i] += amounts[i];
        }

        liquidityShares[msg.sender] = amounts;
    }

    function removeLiquidity() public {
        uint256[] storage userLiquidity = liquidityShares[msg.sender];
        require(userLiquidity.length == tokens.length, "No liquidity provided");

        for (uint256 i = 0; i < tokens.length; i++) {
            uint256 amount = userLiquidity[i];
            require(amount > 0, "No liquidity in token");

            tokens[i].transfer(msg.sender, amount);
            totalLiquidity[i] -= amount;
        }

        delete liquidityShares[msg.sender];
    }
}
