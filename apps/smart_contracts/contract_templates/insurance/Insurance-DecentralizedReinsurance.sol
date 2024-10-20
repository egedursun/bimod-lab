// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DecentralizedReinsurance {
    struct ReinsurancePolicy {
        address insurer;
        uint256 premium;
        uint256 coverageAmount;
        bool active;
    }

    mapping(address => ReinsurancePolicy) public reinsurancePolicies;
    uint256 public totalPremiumCollected;

    event ReinsurancePurchased(address indexed insurer, uint256 premium, uint256 coverageAmount);
    event ReinsuranceClaimPaid(address indexed insurer, uint256 payoutAmount);

    function purchaseReinsurance(uint256 premium, uint256 coverageAmount) public payable {
        require(msg.value == premium, "Incorrect premium payment");
        require(coverageAmount > 0, "Coverage amount must be greater than 0");

        reinsurancePolicies[msg.sender] = ReinsurancePolicy({
            insurer: msg.sender,
            premium: premium,
            coverageAmount: coverageAmount,
            active: true
        });

        totalPremiumCollected += premium;

        emit ReinsurancePurchased(msg.sender, premium, coverageAmount);
    }

    function makeReinsuranceClaim(address insurer) public {
        ReinsurancePolicy storage policy = reinsurancePolicies[insurer];
        require(policy.active, "Reinsurance policy is not active");
        require(policy.coverageAmount <= address(this).balance, "Insufficient funds to pay reinsurance claim");

        policy.active = false;
        payable(insurer).transfer(policy.coverageAmount);

        emit ReinsuranceClaimPaid(insurer, policy.coverageAmount);
    }

    function getReinsurancePolicy(address insurer) public view returns (uint256 premium, uint256 coverageAmount, bool active) {
        ReinsurancePolicy memory policy = reinsurancePolicies[insurer];
        return (policy.premium, policy.coverageAmount, policy.active);
    }
}
