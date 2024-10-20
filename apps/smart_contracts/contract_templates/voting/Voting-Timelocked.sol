// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TimeLockedVoting {
    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
        uint256 unlockTime;
    }

    Proposal[] public proposals;

    event ProposalCreated(uint256 indexed proposalId, string description, uint256 unlockTime);
    event VoteCast(uint256 indexed proposalId, address indexed voter);
    event ProposalExecuted(uint256 indexed proposalId);

    function createProposal(string memory description, uint256 duration) public {
        uint256 unlockTime = block.timestamp + duration;
        proposals.push(Proposal({
            description: description,
            voteCount: 0,
            executed: false,
            unlockTime: unlockTime
        }));

        emit ProposalCreated(proposals.length - 1, description, unlockTime);
    }

    function vote(uint256 proposalId) public {
        require(proposalId < proposals.length, "Invalid proposal");
        require(block.timestamp >= proposals[proposalId].unlockTime, "Voting not yet unlocked");

        proposals[proposalId].voteCount++;
        emit VoteCast(proposalId, msg.sender);
    }

    function executeProposal(uint256 proposalId) public {
        require(proposalId < proposals.length, "Invalid proposal");
        require(proposals[proposalId].voteCount > 0, "No votes cast");
        require(!proposals[proposalId].executed, "Proposal already executed");

        proposals[proposalId].executed = true;

        emit ProposalExecuted(proposalId);
        // Execute proposal logic here, such as contract upgrades or fund transfers.
    }
}
