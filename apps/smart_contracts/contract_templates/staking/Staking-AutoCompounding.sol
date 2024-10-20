// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract AutoCompoundingStaking {
    IERC20 public stakingToken;

    mapping(address => uint256) public stakedBalances;
    mapping(address => uint256) public rewardBalances;

    uint256 public rewardRate;

    constructor(IERC20 _stakingToken, uint256 _rewardRate) {
        stakingToken = _stakingToken;
        rewardRate = _rewardRate;
    }

    function stake(uint256 amount) public {
        require(amount > 0, "Cannot stake 0 tokens");

        stakingToken.transferFrom(msg.sender, address(this), amount);
        stakedBalances[msg.sender] += amount;

        // Auto-compound rewards
        uint256 reward = stakedBalances[msg.sender] * rewardRate;
        stakedBalances[msg.sender] += reward;
    }

    function withdraw(uint256 amount) public {
        require(stakedBalances[msg.sender] >= amount, "Insufficient balance");

        stakedBalances[msg.sender] -= amount;
        stakingToken.transfer(msg.sender, amount);
    }
}
