// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DelegatedVoting {
    struct Voter {
        address delegate;
        bool hasVoted;
        uint256 votes;
    }

    struct Proposal {
        string description;
        uint256 voteCount;
    }

    mapping(address => Voter) public voters;
    Proposal[] public proposals;

    event ProposalCreated(uint256 indexed proposalId, string description);
    event VoteDelegated(address indexed voter, address indexed delegate);
    event VoteCast(address indexed voter, uint256 indexed proposalId);

    function createProposal(string memory description) public {
        proposals.push(Proposal({
            description: description,
            voteCount: 0
        }));

        emit ProposalCreated(proposals.length - 1, description);
    }

    function delegateVote(address delegate) public {
        require(!voters[msg.sender].hasVoted, "Already voted or delegated");
        voters[msg.sender].delegate = delegate;

        emit VoteDelegated(msg.sender, delegate);
    }

    function vote(uint256 proposalId) public {
        Voter storage sender = voters[msg.sender];
        require(!sender.hasVoted, "Already voted");
        require(proposalId < proposals.length, "Invalid proposal");

        if (sender.delegate != address(0)) {
            voters[sender.delegate].votes++;
        } else {
            proposals[proposalId].voteCount++;
        }

        sender.hasVoted = true;

        emit VoteCast(msg.sender, proposalId);
    }
}
