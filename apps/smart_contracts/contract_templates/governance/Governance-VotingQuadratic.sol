// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract QuadraticGovernance {
    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
    }

    Proposal[] public proposals;
    mapping(address => uint256) public votesSpent;

    function createProposal(string memory description) public {
        proposals.push(Proposal({
            description: description,
            voteCount: 0,
            executed: false
        }));
    }

    function vote(uint256 proposalIndex, uint256 numVotes) public {
        require(proposalIndex < proposals.length, "Invalid proposal");
        require(numVotes > 0, "Must vote at least once");

        uint256 cost = numVotes ** 2;  // Quadratic voting cost
        require(votesSpent[msg.sender] + cost <= balanceOf(msg.sender), "Not enough votes");

        proposals[proposalIndex].voteCount += numVotes;
        votesSpent[msg.sender] += cost;
    }

    function executeProposal(uint256 proposalIndex) public {
        require(proposalIndex < proposals.length, "Invalid proposal");
        require(!proposals[proposalIndex].executed, "Proposal already executed");

        proposals[proposalIndex].executed = true;
    }
}
