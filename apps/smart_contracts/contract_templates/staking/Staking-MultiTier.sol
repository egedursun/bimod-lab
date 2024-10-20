// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TieredStaking {
    IERC20 public stakingToken;
    IERC20 public rewardToken;

    struct Tier {
        uint256 minStake;
        uint256 rewardRate;
    }

    Tier[] public tiers;

    mapping(address => uint256) public stakedBalances;
    mapping(address => uint256) public rewardBalances;

    constructor(IERC20 _stakingToken, IERC20 _rewardToken) {
        stakingToken = _stakingToken;
        rewardToken = _rewardToken;

        // Define staking tiers (minStake, rewardRate)
        tiers.push(Tier({minStake: 1000 * 10 ** 18, rewardRate: 50})); // Tier 1
        tiers.push(Tier({minStake: 5000 * 10 ** 18, rewardRate: 100})); // Tier 2
        tiers.push(Tier({minStake: 10000 * 10 ** 18, rewardRate: 200})); // Tier 3
    }

    function stake(uint256 amount) public {
        require(amount > 0, "Cannot stake 0 tokens");

        stakingToken.transferFrom(msg.sender, address(this), amount);
        stakedBalances[msg.sender] += amount;

        uint256 rewardRate = getRewardRate(amount);
        rewardBalances[msg.sender] += amount * rewardRate;
    }

    function withdraw(uint256 amount) public {
        require(stakedBalances[msg.sender] >= amount, "Insufficient balance");

        stakedBalances[msg.sender] -= amount;
        stakingToken.transfer(msg.sender, amount);
    }

    function claimReward() public {
        uint256 reward = rewardBalances[msg.sender];
        rewardBalances[msg.sender] = 0;
        rewardToken.transfer(msg.sender, reward);
    }

    function getRewardRate(uint256 amount) public view returns (uint256) {
        for (uint256 i = tiers.length - 1; i >= 0; i--) {
            if (amount >= tiers[i].minStake) {
                return tiers[i].rewardRate;
            }
        }
        return 0;
    }
}
