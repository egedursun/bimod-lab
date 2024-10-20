// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract WeightedVoting {
    struct Proposal {
        string description;
        uint256 totalWeight;
        bool executed;
    }

    mapping(address => uint256) public voterWeights;
    mapping(address => mapping(uint256 => bool)) public hasVoted;

    Proposal[] public proposals;

    event ProposalCreated(uint256 indexed proposalId, string description);
    event Voted(uint256 indexed proposalId, address indexed voter, uint256 weight);

    constructor(address[] memory voters, uint256[] memory weights) {
        require(voters.length == weights.length, "Mismatched voters and weights");
        for (uint256 i = 0; i < voters.length; i++) {
            voterWeights[voters[i]] = weights[i];
        }
    }

    function createProposal(string memory description) public {
        proposals.push(Proposal({
            description: description,
            totalWeight: 0,
            executed: false
        }));

        emit ProposalCreated(proposals.length - 1, description);
    }

    function vote(uint256 proposalId) public {
        require(voterWeights[msg.sender] > 0, "No voting power");
        require(!hasVoted[msg.sender][proposalId], "Already voted");
        require(proposalId < proposals.length, "Invalid proposal");

        proposals[proposalId].totalWeight += voterWeights[msg.sender];
        hasVoted[msg.sender][proposalId] = true;

        emit Voted(proposalId, msg.sender, voterWeights[msg.sender]);
    }
}
