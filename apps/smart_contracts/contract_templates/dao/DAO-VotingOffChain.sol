// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract OffChainVotingDAO {
    address public owner;
    mapping(bytes32 => Proposal) public proposals;
    mapping(bytes32 => bool) public proposalExecuted;

    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
    }

    event ProposalCreated(bytes32 indexed proposalId, string description);
    event ProposalExecuted(bytes32 indexed proposalId);

    constructor() {
        owner = msg.sender;
    }

    function createProposal(bytes32 proposalId, string memory description) public {
        require(msg.sender == owner, "Only owner can create proposals");
        require(proposals[proposalId].voteCount == 0, "Proposal already exists");

        proposals[proposalId] = Proposal({
            description: description,
            voteCount: 0,
            executed: false
        });

        emit ProposalCreated(proposalId, description);
    }

    function executeProposal(bytes32 proposalId) public {
        require(msg.sender == owner, "Only owner can execute proposals");
        require(!proposals[proposalId].executed, "Proposal already executed");
        require(proposals[proposalId].voteCount > 0, "No votes received");

        proposals[proposalId].executed = true;
        proposalExecuted[proposalId] = true;

        emit ProposalExecuted(proposalId);
    }
}
