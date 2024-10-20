// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TokenBasedDAOVoting {
    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
    }

    IERC20 public governanceToken;
    Proposal[] public proposals;

    mapping(address => bool) public hasVoted;

    constructor(address _governanceToken) {
        governanceToken = IERC20(_governanceToken);
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

        uint256 voteWeight = governanceToken.balanceOf(msg.sender);
        proposals[proposalIndex].voteCount += voteWeight;
        hasVoted[msg.sender] = true;
    }

    function executeProposal(uint256 proposalIndex) public {
        require(proposalIndex < proposals.length, "Invalid proposal");
        require(!proposals[proposalIndex].executed, "Proposal already executed");

        proposals[proposalIndex].executed = true;
    }
}
