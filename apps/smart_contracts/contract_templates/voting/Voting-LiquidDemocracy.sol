// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LiquidDemocracy {
    struct Voter {
        address delegate;
        bool hasVoted;
        uint256 voteWeight;
    }

    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
    }

    mapping(address => Voter) public voters;
    Proposal[] public proposals;

    event ProposalCreated(uint256 indexed proposalId, string description);
    event VoteDelegated(address indexed voter, address indexed delegate);
    event VoteCast(address indexed voter, uint256 indexed proposalId);

    function createProposal(string memory description) public {
        proposals.push(Proposal({
            description: description,
            voteCount: 0,
            executed: false
        }));

        emit ProposalCreated(proposals.length - 1, description);
    }

    function delegateVote(address delegate) public {
        require(!voters[msg.sender].hasVoted, "Already voted");
        voters[msg.sender].delegate = delegate;

        emit VoteDelegated(msg.sender, delegate);
    }

    function vote(uint256 proposalId) public {
        Voter storage sender = voters[msg.sender];
        require(!sender.hasVoted, "Already voted");
        require(proposalId < proposals.length, "Invalid proposal");

        if (sender.delegate != address(0)) {
            voters[sender.delegate].voteWeight++;
        } else {
            proposals[proposalId].voteCount++;
        }

        sender.hasVoted = true;

        emit VoteCast(msg.sender, proposalId);
    }

    function getVoteCount(uint256 proposalId) public view returns (uint256) {
        return proposals[proposalId].voteCount;
    }
}
