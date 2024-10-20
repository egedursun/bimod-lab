// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MultiSigVoting {
    address[] public signers;
    uint256 public requiredSignatures;

    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
        mapping(address => bool) voted;
    }

    Proposal[] public proposals;

    event ProposalCreated(uint256 indexed proposalId, string description);
    event VoteCast(uint256 indexed proposalId, address indexed voter);
    event ProposalExecuted(uint256 indexed proposalId);

    constructor(address[] memory _signers, uint256 _requiredSignatures) {
        signers = _signers;
        requiredSignatures = _requiredSignatures;
    }

    modifier onlySigner() {
        bool isSigner = false;
        for (uint256 i = 0; i < signers.length; i++) {
            if (signers[i] == msg.sender) {
                isSigner = true;
                break;
            }
        }
        require(isSigner, "Not an authorized signer");
        _;
    }

    function createProposal(string memory description) public onlySigner {
        proposals.push();
        Proposal storage newProposal = proposals[proposals.length - 1];
        newProposal.description = description;
        newProposal.voteCount = 0;
        newProposal.executed = false;

        emit ProposalCreated(proposals.length - 1, description);
    }

    function vote(uint256 proposalId) public onlySigner {
        Proposal storage proposal = proposals[proposalId];
        require(!proposal.voted[msg.sender], "Already voted");
        proposal.voted[msg.sender] = true;
        proposal.voteCount++;

        emit VoteCast(proposalId, msg.sender);

        if (proposal.voteCount >= requiredSignatures) {
            executeProposal(proposalId);
        }
    }

    function executeProposal(uint256 proposalId) internal {
        Proposal storage proposal = proposals[proposalId];
        require(!proposal.executed, "Proposal already executed");
        proposal.executed = true;

        emit ProposalExecuted(proposalId);
        // Execute proposal logic here.
    }
}
