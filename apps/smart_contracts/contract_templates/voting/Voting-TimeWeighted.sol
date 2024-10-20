// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TimeWeightedVoting {
    struct Voter {
        uint256 tokenBalance;
        uint256 startTime;
    }

    struct Proposal {
        string description;
        uint256 totalWeight;
        bool executed;
    }

    mapping(address => Voter) public voters;
    Proposal[] public proposals;

    event ProposalCreated(uint256 indexed proposalId, string description);
    event Voted(uint256 indexed proposalId, address indexed voter, uint256 weight);

    function createProposal(string memory description) public {
        proposals.push(Proposal({
            description: description,
            totalWeight: 0,
            executed: false
        }));

        emit ProposalCreated(proposals.length - 1, description);
    }

    function registerVoter(address voter, uint256 tokenBalance) public {
        voters[voter] = Voter({
            tokenBalance: tokenBalance,
            startTime: block.timestamp
        });
    }

    function vote(uint256 proposalId) public {
        require(proposalId < proposals.length, "Invalid proposal");

        Voter memory voter = voters[msg.sender];
        require(voter.tokenBalance > 0, "No tokens");

        uint256 votingWeight = voter.tokenBalance * (block.timestamp - voter.startTime);
        proposals[proposalId].totalWeight += votingWeight;

        emit Voted(proposalId, msg.sender, votingWeight);
    }
}
