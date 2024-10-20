// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualInsurance {
    struct Member {
        bool isMember;
        uint256 contribution;
    }

    mapping(address => Member) public members;
    uint256 public totalPool;
    address public admin;

    event MemberJoined(address indexed member, uint256 contribution);
    event ClaimApproved(address indexed member, uint256 payoutAmount);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can approve claims");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    function joinMutual(uint256 contribution) public payable {
        require(msg.value == contribution, "Incorrect contribution amount");
        require(!members[msg.sender].isMember, "Already a member");

        members[msg.sender] = Member({
            isMember: true,
            contribution: contribution
        });

        totalPool += contribution;

        emit MemberJoined(msg.sender, contribution);
    }

    function approveClaim(address member, uint256 payoutAmount) public onlyAdmin {
        require(members[member].isMember, "Not a member");
        require(payoutAmount <= totalPool, "Insufficient pool balance");

        totalPool -= payoutAmount;
        payable(member).transfer(payoutAmount);

        emit ClaimApproved(member, payoutAmount);
    }

    function getPoolBalance() public view returns (uint256) {
        return totalPool;
    }
}
