// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract BasicGovernance {
    IERC20 public governanceToken;

    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
    }

    Proposal[] public proposals;
    mapping(address => bool) public hasVoted;

    constructor(IERC20 _governanceToken) {
        governanceToken = _governanceToken;
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

        uint256 votePower = governanceToken.balanceOf(msg.sender);
        proposals[proposalIndex].voteCount += votePower;
        hasVoted[msg.sender] = true;
    }

    function executeProposal(uint256 proposalIndex) public {
        require(proposalIndex < proposals.length, "Invalid proposal");
        require(!proposals[proposalIndex].executed, "Proposal already executed");

        proposals[proposalIndex].executed = true;
    }
}
