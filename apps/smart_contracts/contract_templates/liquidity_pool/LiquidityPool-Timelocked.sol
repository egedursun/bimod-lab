// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TimeLockedLiquidityPool {
    IERC20 public lpToken;
    IERC20 public rewardToken;

    struct Stake {
        uint256 amount;
        uint256 lockEndTime;
    }

    mapping(address => Stake) public stakes;
    uint256 public rewardRate;
    uint256 public lockDuration;

    constructor(IERC20 _lpToken, IERC20 _rewardToken, uint256 _rewardRate, uint256 _lockDuration) {
        lpToken = _lpToken;
        rewardToken = _rewardToken;
        rewardRate = _rewardRate;
        lockDuration = _lockDuration;
    }

    function stake(uint256 amount) public {
        require(amount > 0, "Cannot stake 0 LP tokens");

        lpToken.transferFrom(msg.sender, address(this), amount);
        stakes[msg.sender] = Stake({
            amount: amount,
            lockEndTime: block.timestamp + lockDuration
        });
    }

    function withdraw() public {
        Stake storage userStake = stakes[msg.sender];
        require(block.timestamp >= userStake.lockEndTime, "Lock period not over");

        uint256 amount = userStake.amount;
        userStake.amount = 0;

        lpToken.transfer(msg.sender, amount);
    }

    function claimReward() public {
        Stake storage userStake = stakes[msg.sender];
        require(userStake.amount > 0, "No staked tokens");

        uint256 reward = userStake.amount * rewardRate;
        rewardToken.transfer(msg.sender, reward);
    }
}
