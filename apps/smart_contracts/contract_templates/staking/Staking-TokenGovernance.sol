// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract GovernanceTokenStaking {
    IERC20 public governanceToken;

    mapping(address => uint256) public stakedBalances;
    mapping(address => uint256) public votingPower;

    uint256 public totalStaked;

    constructor(IERC20 _governanceToken) {
        governanceToken = _governanceToken;
    }

    function stake(uint256 amount) public {
        require(amount > 0, "Cannot stake 0 tokens");

        governanceToken.transferFrom(msg.sender, address(this), amount);
        stakedBalances[msg.sender] += amount;
        totalStaked += amount;

        updateVotingPower(msg.sender);
    }

    function withdraw(uint256 amount) public {
        require(stakedBalances[msg.sender] >= amount, "Insufficient balance");

        stakedBalances[msg.sender] -= amount;
        totalStaked -= amount;
        governanceToken.transfer(msg.sender, amount);

        updateVotingPower(msg.sender);
    }

    function updateVotingPower(address staker) internal {
        votingPower[staker] = (stakedBalances[staker] * 100) / totalStaked;
    }
}
