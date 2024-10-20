// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract DynamicVotingPowerGovernance {
    IERC20 public governanceToken;
    uint256 public proposalDuration;

    struct Proposal {
        string description;
        uint256 voteCount;
        uint256 deadline;
        bool executed;
    }

    Proposal[] public proposals;
    mapping(address => uint256) public tokenHoldTimestamps;

    constructor(IERC20 _governanceToken, uint256 _proposalDuration) {
        governanceToken = _governanceToken;
        proposalDuration = _proposalDuration;
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

        uint256 heldTime = block.timestamp - tokenHoldTimestamps[msg.sender];
        uint256 votePower = governanceToken.balanceOf(msg.sender) * heldTime;  // Time-weighted voting power

        proposals[proposalIndex].voteCount += votePower;
    }

    function executeProposal(uint256 proposalIndex) public {
        Proposal storage proposal = proposals[proposalIndex];
        require(block.timestamp >= proposal.deadline, "Voting period not ended");
        require(!proposal.executed, "Proposal already executed");

        proposal.executed = true;
    }

    function updateHoldTimestamp(address holder) public {
        tokenHoldTimestamps[holder] = block.timestamp;
    }
}
