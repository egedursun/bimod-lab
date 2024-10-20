// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract YieldFarmingStaking {
    IERC20 public lpToken;
    IERC20 public rewardToken;

    mapping(address => uint256) public stakedBalances;
    mapping(address => uint256) public rewardBalances;

    uint256 public totalStaked;
    uint256 public rewardRate;

    constructor(IERC20 _lpToken, IERC20 _rewardToken, uint256 _rewardRate) {
        lpToken = _lpToken;
        rewardToken = _rewardToken;
        rewardRate = _rewardRate;
    }

    function stake(uint256 amount) public {
        require(amount > 0, "Cannot stake 0 tokens");

        lpToken.transferFrom(msg.sender, address(this), amount);
        stakedBalances[msg.sender] += amount;
        totalStaked += amount;
    }

    function withdraw(uint256 amount) public {
        require(stakedBalances[msg.sender] >= amount, "Insufficient balance");

        stakedBalances[msg.sender] -= amount;
        totalStaked -= amount;
        lpToken.transfer(msg.sender, amount);
    }

    function claimReward() public {
        uint256 reward = stakedBalances[msg.sender] * rewardRate;
        rewardBalances[msg.sender] += reward;
        rewardToken.transfer(msg.sender, reward);
    }
}
