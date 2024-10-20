// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BasicDAOVoting {
    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
    }

    address public owner;
    Proposal[] public proposals;
    mapping(address => bool) public hasVoted;

    constructor() {
        owner = msg.sender;
    }

    function createProposal(string memory description) public {
        proposals.push(Proposal({
            description: description,
            voteCount: 0,
            executed: false
        }));
    }

    function vote(uint256 proposalIndex) public {
        require(!hasVoted[msg.sender], "Already voted");
        require(proposalIndex < proposals.length, "Invalid proposal");

        proposals[proposalIndex].voteCount += 1;
        hasVoted[msg.sender] = true;
    }

    function executeProposal(uint256 proposalIndex) public {
        require(msg.sender == owner, "Only owner can execute");
        require(proposalIndex < proposals.length, "Invalid proposal");
        require(!proposals[proposalIndex].executed, "Proposal already executed");

        proposals[proposalIndex].executed = true;
    }
}
