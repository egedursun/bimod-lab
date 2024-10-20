// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract QuorumGovernance {
    IERC20 public governanceToken;
    uint256 public quorumPercentage;  // e.g., 10 means 10% of total supply
    uint256 public proposalDuration;

    struct Proposal {
        string description;
        uint256 voteCount;
        uint256 deadline;
        bool executed;
    }

    Proposal[] public proposals;
    uint256 public totalTokenSupply;

    constructor(IERC20 _governanceToken, uint256 _quorumPercentage, uint256 _proposalDuration) {
        governanceToken = _governanceToken;
        quorumPercentage = _quorumPercentage;
        proposalDuration = _proposalDuration;
        totalTokenSupply = governanceToken.totalSupply();
    }

    function createProposal(string memory description) public {
        proposals.push(Proposal({
            description: description,
            voteCount: 0,
            deadline: block.timestamp + proposalDuration,
            executed: false
        }));
    }

    function vote(uint256 proposalIndex) public {
        require(proposalIndex < proposals.length, "Invalid proposal");
        require(block.timestamp < proposals[proposalIndex].deadline, "Voting period over");

        uint256 votePower = governanceToken.balanceOf(msg.sender);
        proposals[proposalIndex].voteCount += votePower;
    }

    function executeProposal(uint256 proposalIndex) public {
        Proposal storage proposal = proposals[proposalIndex];
        require(block.timestamp >= proposal.deadline, "Voting period not ended");
        require(!proposal.executed, "Proposal already executed");

        uint256 quorum = (totalTokenSupply * quorumPercentage) / 100;
        require(proposal.voteCount >= quorum, "Quorum not met");

        proposal.executed = true;
    }
}
