// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract StakingProtocol {
    IERC20 public stakingToken;
    IERC20 public rewardToken;

    struct Stake {
        uint256 amount;
        uint256 rewardDebt;
    }

    mapping(address => Stake) public stakes;
    uint256 public rewardRate;
    uint256 public totalStaked;

    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount);
    event RewardClaimed(address indexed user, uint256 reward);

    constructor(IERC20 _stakingToken, IERC20 _rewardToken, uint256 _rewardRate) {
        stakingToken = _stakingToken;
        rewardToken = _rewardToken;
        rewardRate = _rewardRate;
    }

    function stake(uint256 amount) public {
        require(amount > 0, "Cannot stake 0 tokens");

        stakingToken.transferFrom(msg.sender, address(this), amount);
        totalStaked += amount;

        stakes[msg.sender].amount += amount;
        stakes[msg.sender].rewardDebt += (amount * rewardRate);

        emit Staked(msg.sender, amount);
    }

    function unstake(uint256 amount) public {
        require(stakes[msg.sender].amount >= amount, "Insufficient staked amount");

        totalStaked -= amount;
        stakes[msg.sender].amount -= amount;

        stakingToken.transfer(msg.sender, amount);
        emit Unstaked(msg.sender, amount);
    }

    function claimReward() public {
        uint256 reward = stakes[msg.sender].rewardDebt;
        require(reward > 0, "No reward available");

        rewardToken.transfer(msg.sender, reward);
        stakes[msg.sender].rewardDebt = 0;

        emit RewardClaimed(msg.sender, reward);
    }
}
