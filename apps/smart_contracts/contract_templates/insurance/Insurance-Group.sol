// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GroupInsurance {
    struct GroupPolicy {
        address organizer;
        uint256 premium;
        uint256 coverageAmount;
        address[] members;
        bool active;
    }

    mapping(address => GroupPolicy) public groupPolicies;

    event GroupPolicyPurchased(address indexed organizer, uint256 premium, uint256 coverageAmount, address[] members);
    event GroupClaimPaid(address indexed organizer, address indexed member, uint256 payoutAmount);

    function purchaseGroupPolicy(uint256 premium, uint256 coverageAmount, address[] memory members) public payable {
        require(msg.value == premium, "Incorrect premium payment");
        require(coverageAmount > 0, "Coverage amount must be greater than 0");

        groupPolicies[msg.sender] = GroupPolicy({
            organizer: msg.sender,
            premium: premium,
            coverageAmount: coverageAmount,
            members: members,
            active: true
        });

        emit GroupPolicyPurchased(msg.sender, premium, coverageAmount, members);
    }

    function makeGroupClaim(address member, uint256 payoutAmount) public {
        GroupPolicy storage policy = groupPolicies[msg.sender];
        require(policy.active, "Group policy is not active");
        require(payoutAmount <= address(this).balance, "Insufficient funds to pay claim");

        payable(member).transfer(payoutAmount);

        emit GroupClaimPaid(msg.sender, member, payoutAmount);
    }

    function getGroupMembers(address organizer) public view returns (address[] memory) {
        return groupPolicies[organizer].members;
    }
}
