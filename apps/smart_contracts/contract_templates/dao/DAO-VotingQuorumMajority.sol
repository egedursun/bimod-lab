// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DAOWithQuorum {
    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
        uint256 deadline;
    }

    uint256 public quorumPercentage;
    uint256 public proposalDuration;
    uint256 public totalMembers;
    mapping(address => bool) public members;
    Proposal[] public proposals;
    mapping(uint256 => mapping(address => bool)) public hasVoted;

    constructor(uint256 _quorumPercentage, uint256 _proposalDuration) {
        quorumPercentage = _quorumPercentage;
        proposalDuration = _proposalDuration;
        totalMembers = 0;
    }

    function addMember(address newMember) public {
        members[newMember] = true;
        totalMembers++;
    }

    function createProposal(string memory description) public {
        require(members[msg.sender], "Not a DAO member");

        proposals.push(Proposal({
            description: description,
            voteCount: 0,
            executed: false,
            deadline: block.timestamp + proposalDuration
        }));
    }

    function vote(uint256 proposalIndex) public {
        require(members[msg.sender], "Not a DAO member");
        require(!hasVoted[proposalIndex][msg.sender], "Already voted");
        require(block.timestamp < proposals[proposalIndex].deadline, "Voting period is over");

        proposals[proposalIndex].voteCount++;
        hasVoted[proposalIndex][msg.sender] = true;
    }

    function executeProposal(uint256 proposalIndex) public {
        require(block.timestamp >= proposals[proposalIndex].deadline, "Voting period not over");
        require(!proposals[proposalIndex].executed, "Proposal already executed");

        uint256 quorum = (totalMembers * quorumPercentage) / 100;
        require(proposals[proposalIndex].voteCount >= quorum, "Quorum not reached");

        proposals[proposalIndex].executed = true;
    }
}
