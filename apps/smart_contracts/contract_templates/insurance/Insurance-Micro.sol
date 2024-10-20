// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Microinsurance {
    struct Policy {
        address policyholder;
        uint256 premium;
        uint256 coverageAmount;
        bool active;
    }

    mapping(address => Policy) public policies;
    uint256 public totalPremiumCollected;

    event MicroPolicyPurchased(address indexed policyholder, uint256 premium, uint256 coverageAmount);
    event MicroClaimPaid(address indexed policyholder, uint256 payoutAmount);

    function purchasePolicy(uint256 premium, uint256 coverageAmount) public payable {
        require(msg.value == premium, "Incorrect premium payment");
        require(coverageAmount > 0, "Coverage amount must be greater than 0");

        policies[msg.sender] = Policy({
            policyholder: msg.sender,
            premium: premium,
            coverageAmount: coverageAmount,
            active: true
        });

        totalPremiumCollected += premium;

        emit MicroPolicyPurchased(msg.sender, premium, coverageAmount);
    }

    function makeMicroClaim(address policyholder) public {
        Policy storage policy = policies[policyholder];
        require(policy.active, "Policy is not active");
        require(policy.coverageAmount <= address(this).balance, "Insufficient funds to pay claim");

        policy.active = false;
        payable(policyholder).transfer(policy.coverageAmount);

        emit MicroClaimPaid(policyholder, policy.coverageAmount);
    }

    function getPolicyDetails(address policyholder) public view returns (uint256 premium, uint256 coverageAmount, bool active) {
        Policy memory policy = policies[policyholder];
        return (policy.premium, policy.coverageAmount, policy.active);
    }
}
