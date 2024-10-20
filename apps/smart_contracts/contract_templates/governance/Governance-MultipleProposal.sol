// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MultiTypeGovernance {
    enum ProposalType { FUND_ALLOCATION, PROTOCOL_CHANGE }
    struct Proposal {
        string description;
        ProposalType proposalType;
        uint256 voteCount;
        bool executed;
    }

    Proposal[] public proposals;
    mapping(ProposalType => uint256) public quorumRequirements;

    constructor() {
        // Set quorum requirements for each proposal type
        quorumRequirements[ProposalType.FUND_ALLOCATION] = 100;
        quorumRequirements[ProposalType.PROTOCOL_CHANGE] = 200;
    }

    function createProposal(string memory description, ProposalType proposalType) public {
        proposals.push(Proposal({
            description: description,
            proposalType: proposalType,
            voteCount: 0,
            executed: false
        }));
    }

    function vote(uint256 proposalIndex) public {
        require(proposalIndex < proposals.length, "Invalid proposal");

        Proposal storage proposal = proposals[proposalIndex];
        proposal.voteCount++;
    }

    function executeProposal(uint256 proposalIndex) public {
        Proposal storage proposal = proposals[proposalIndex];
        require(!proposal.executed, "Proposal already executed");

        uint256 quorum = quorumRequirements[proposal.proposalType];
        require(proposal.voteCount >= quorum, "Quorum not reached");

        proposal.executed = true;
    }
}
