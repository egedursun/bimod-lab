// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract YieldFarming {
    IERC20 public lpToken;
    IERC20 public rewardToken;

    mapping(address => uint256) public userBalances;
    mapping(address => uint256) public rewardDebts;
    uint256 public totalLiquidity;
    uint256 public rewardRate;

    event LiquidityProvided(address indexed user, uint256 amount);
    event LiquidityWithdrawn(address indexed user, uint256 amount);
    event RewardClaimed(address indexed user, uint256 amount);

    constructor(IERC20 _lpToken, IERC20 _rewardToken, uint256 _rewardRate) {
        lpToken = _lpToken;
        rewardToken = _rewardToken;
        rewardRate = _rewardRate;
    }

    function provideLiquidity(uint256 amount) public {
        require(amount > 0, "Cannot provide 0 liquidity");

        lpToken.transferFrom(msg.sender, address(this), amount);
        totalLiquidity += amount;
        userBalances[msg.sender] += amount;

        emit LiquidityProvided(msg.sender, amount);
    }

    function withdrawLiquidity(uint256 amount) public {
        require(userBalances[msg.sender] >= amount, "Insufficient liquidity");

        totalLiquidity -= amount;
        userBalances[msg.sender] -= amount;

        lpToken.transfer(msg.sender, amount);
        emit LiquidityWithdrawn(msg.sender, amount);
    }

    function claimReward() public {
        uint256 reward = userBalances[msg.sender] * rewardRate;
        require(reward > 0, "No rewards available");

        rewardToken.transfer(msg.sender, reward);
        rewardDebts[msg.sender] += reward;

        emit RewardClaimed(msg.sender, reward);
    }
}
