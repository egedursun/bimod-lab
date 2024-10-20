// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TimeLockedStaking {
    IERC20 public stakingToken;
    IERC20 public rewardToken;

    struct Stake {
        uint256 amount;
        uint256 startTime;
    }

    mapping(address => Stake) public stakes;
    uint256 public lockDuration;
    uint256 public rewardRate;

    constructor(IERC20 _stakingToken, IERC20 _rewardToken, uint256 _lockDuration, uint256 _rewardRate) {
        stakingToken = _stakingToken;
        rewardToken = _rewardToken;
        lockDuration = _lockDuration;
        rewardRate = _rewardRate;
    }

    function stake(uint256 amount) public {
        require(amount > 0, "Cannot stake 0 tokens");

        stakingToken.transferFrom(msg.sender, address(this), amount);
        stakes[msg.sender] = Stake({
            amount: amount,
            startTime: block.timestamp
        });
    }

    function withdraw() public {
        Stake storage stakeInfo = stakes[msg.sender];
        require(block.timestamp >= stakeInfo.startTime + lockDuration, "Tokens are still locked");

        uint256 amount = stakeInfo.amount;
        stakeInfo.amount = 0;
        stakingToken.transfer(msg.sender, amount);
    }

    function claimReward() public {
        Stake storage stakeInfo = stakes[msg.sender];
        require(block.timestamp >= stakeInfo.startTime + lockDuration, "Cannot claim rewards until lock period ends");

        uint256 reward = stakeInfo.amount * rewardRate;
        rewardToken.transfer(msg.sender, reward);
    }
}
