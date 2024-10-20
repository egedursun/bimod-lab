// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract MultiAssetStaking {
    IERC20 public rewardToken;
    IERC20[] public stakingTokens;

    struct StakedAsset {
        uint256 amount;
        uint256 rewardRate;
    }

    mapping(address => mapping(IERC20 => StakedAsset)) public stakedBalances;

    constructor(IERC20[] memory _stakingTokens, IERC20 _rewardToken) {
        stakingTokens = _stakingTokens;
        rewardToken = _rewardToken;
    }

    function stake(IERC20 token, uint256 amount) public {
        require(isValidToken(token), "Invalid staking token");
        require(amount > 0, "Cannot stake 0 tokens");

        token.transferFrom(msg.sender, address(this), amount);
        stakedBalances[msg.sender][token].amount += amount;
    }

    function withdraw(IERC20 token, uint256 amount) public {
        require(stakedBalances[msg.sender][token].amount >= amount, "Insufficient balance");

        stakedBalances[msg.sender][token].amount -= amount;
        token.transfer(msg.sender, amount);
    }

    function claimReward() public {
        uint256 totalReward = 0;

        for (uint256 i = 0; i < stakingTokens.length; i++) {
            IERC20 token = stakingTokens[i];
            StakedAsset storage asset = stakedBalances[msg.sender][token];
            uint256 reward = asset.amount * asset.rewardRate;
            totalReward += reward;
        }

        rewardToken.transfer(msg.sender, totalReward);
    }

    function isValidToken(IERC20 token) internal view returns (bool) {
        for (uint256 i = 0; i < stakingTokens.length; i++) {
            if (stakingTokens[i] == token) {
                return true;
            }
        }
        return false;
    }
}
