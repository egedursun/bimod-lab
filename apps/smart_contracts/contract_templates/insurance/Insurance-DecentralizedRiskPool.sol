// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DecentralizedRiskPool {
    struct Policy {
        address policyholder;
        uint256 premium;
        uint256 payoutAmount;
        bool active;
    }

    mapping(address => Policy) public policies;
    address[] public poolContributors;
    uint256 public poolBalance;

    event PolicyCreated(address indexed policyholder, uint256 premium, uint256 payoutAmount);
    event ClaimPaid(address indexed policyholder, uint256 payoutAmount);
    event ContributionAdded(address indexed contributor, uint256 amount);

    function createPolicy(uint256 premium, uint256 payoutAmount) public payable {
        require(msg.value == premium, "Incorrect premium payment");

        policies[msg.sender] = Policy({
            policyholder: msg.sender,
            premium: premium,
            payoutAmount: payoutAmount,
            active: true
        });

        poolBalance += msg.value;
        emit PolicyCreated(msg.sender, premium, payoutAmount);
    }

    function addToPool() public payable {
        require(msg.value > 0, "Must contribute positive amount");
        poolContributors.push(msg.sender);
        poolBalance += msg.value;

        emit ContributionAdded(msg.sender, msg.value);
    }

    function makeClaim(address policyholder) public {
        Policy storage policy = policies[policyholder];
        require(policy.active, "Policy is not active");
        require(poolBalance >= policy.payoutAmount, "Insufficient pool balance");

        policy.active = false;
        poolBalance -= policy.payoutAmount;
        payable(policy.policyholder).transfer(policy.payoutAmount);

        emit ClaimPaid(policy.policyholder, policy.payoutAmount);
    }

    function getPoolBalance() public view returns (uint256) {
        return poolBalance;
    }
}
