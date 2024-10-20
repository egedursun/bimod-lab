// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InsuranceStaking {
    struct Staker {
        uint256 stakedAmount;
        uint256 reward;
    }

    mapping(address => Staker) public stakers;
    uint256 public totalStaked;

    event Staked(address indexed staker, uint256 amount);
    event RewardPaid(address indexed staker, uint256 reward);
    event ClaimCovered(address indexed claimant, uint256 payoutAmount);

    function stake() public payable {
        require(msg.value > 0, "Stake amount must be greater than 0");

        stakers[msg.sender].stakedAmount += msg.value;
        totalStaked += msg.value;

        emit Staked(msg.sender, msg.value);
    }

    function payClaim(address claimant, uint256 payoutAmount) public {
        require(totalStaked >= payoutAmount, "Insufficient staked funds");

        uint256 individualContribution = payoutAmount / totalStaked;
        totalStaked -= payoutAmount;

        payable(claimant).transfer(payoutAmount);

        emit ClaimCovered(claimant, payoutAmount);
    }

    function withdrawReward(uint256 reward) public {
        require(stakers[msg.sender].reward >= reward, "Insufficient reward balance");

        stakers[msg.sender].reward -= reward;
        payable(msg.sender).transfer(reward);

        emit RewardPaid(msg.sender, reward);
    }

    function getStakedAmount(address staker) public view returns (uint256) {
        return stakers[staker].stakedAmount;
    }

    function getTotalStaked() public view returns (uint256) {
        return totalStaked;
    }
}
