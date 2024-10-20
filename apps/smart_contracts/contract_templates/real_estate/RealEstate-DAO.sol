// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RealEstateDAO {
    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
    }

    mapping(uint256 => Proposal) public proposals;
    mapping(address => uint256) public votingPower;
    uint256 public proposalCount;
    address public daoOwner;

    event ProposalCreated(uint256 proposalId, string description);
    event Voted(address indexed voter, uint256 proposalId);
    event ProposalExecuted(uint256 proposalId);

    constructor() {
        daoOwner = msg.sender;
    }

    function addVotingPower(address tokenHolder, uint256 power) public {
        require(msg.sender == daoOwner, "Only DAO owner can add voting power");
        votingPower[tokenHolder] += power;
    }

    function createProposal(string memory description) public {
        proposalCount++;
        proposals[proposalCount] = Proposal(description, 0, false);

        emit ProposalCreated(proposalCount, description);
    }

    function vote(uint256 proposalId) public {
        require(votingPower[msg.sender] > 0, "No voting power");
        require(!proposals[proposalId].executed, "Proposal already executed");

        proposals[proposalId].voteCount += votingPower[msg.sender];
        emit Voted(msg.sender, proposalId);
    }

    function executeProposal(uint256 proposalId) public {
        Proposal storage proposal = proposals[proposalId];
        require(proposal.voteCount > 50, "Not enough votes to execute");
        require(!proposal.executed, "Proposal already executed");

        proposal.executed = true;

        // Execute proposal logic (e.g., purchase property, make upgrades)
        emit ProposalExecuted(proposalId);
    }
}
