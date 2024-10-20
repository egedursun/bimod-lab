// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract YieldFarmingLiquidityPool {
    IERC20 public lpToken;
    IERC20 public rewardToken;

    mapping(address => uint256) public depositedTokens;
    mapping(address => uint256) public rewardDebt;

    uint256 public totalDeposited;
    uint256 public rewardPerTokenStored;
    uint256 public lastUpdateTime;
    uint256 public rewardRate;

    constructor(IERC20 _lpToken, IERC20 _rewardToken, uint256 _rewardRate) {
        lpToken = _lpToken;
        rewardToken = _rewardToken;
        rewardRate = _rewardRate;
        lastUpdateTime = block.timestamp;
    }

    function deposit(uint256 amount) public {
        updateRewards();

        lpToken.transferFrom(msg.sender, address(this), amount);
        totalDeposited += amount;
        depositedTokens[msg.sender] += amount;
        rewardDebt[msg.sender] = depositedTokens[msg.sender] * rewardPerTokenStored;
    }

    function withdraw(uint256 amount) public {
        updateRewards();

        require(depositedTokens[msg.sender] >= amount, "Insufficient deposit");

        depositedTokens[msg.sender] -= amount;
        totalDeposited -= amount;
        lpToken.transfer(msg.sender, amount);

        rewardDebt[msg.sender] = depositedTokens[msg.sender] * rewardPerTokenStored;
    }

    function claimRewards() public {
        updateRewards();

        uint256 pendingRewards = depositedTokens[msg.sender] * rewardPerTokenStored - rewardDebt[msg.sender];
        rewardDebt[msg.sender] = depositedTokens[msg.sender] * rewardPerTokenStored;

        rewardToken.transfer(msg.sender, pendingRewards);
    }

    function updateRewards() internal {
        if (totalDeposited > 0) {
            rewardPerTokenStored += (block.timestamp - lastUpdateTime) * rewardRate / totalDeposited;
        }
        lastUpdateTime = block.timestamp;
    }
}
