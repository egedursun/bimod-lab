// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract VestingGovernance {
    IERC20 public governanceToken;
    uint256 public vestingDuration;

    struct VestingSchedule {
        uint256 startTime;
        uint256 amount;
    }

    mapping(address => VestingSchedule) public vestingSchedules;

    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
    }

    Proposal[] public proposals;

    constructor(IERC20 _governanceToken, uint256 _vestingDuration) {
        governanceToken = _governanceToken;
        vestingDuration = _vestingDuration;
    }

    // Function to add vesting schedules for token holders
    function addVestingSchedule(address voter, uint256 amount) public {
        vestingSchedules[voter] = VestingSchedule({
            startTime: block.timestamp,
            amount: amount
        });
    }

    // Function to create a new governance proposal
    function createProposal(string memory description) public {
        proposals.push(Proposal({
            description: description,
            voteCount: 0,
            executed: false
        }));
    }

    // Function to vote on a proposal, only vested tokens can be used to vote
    function vote(uint256 proposalIndex) public {
        require(proposalIndex < proposals.length, "Invalid proposal");

        VestingSchedule storage schedule = vestingSchedules[msg.sender];
        require(block.timestamp >= schedule.startTime + vestingDuration, "Tokens are still vesting");

        uint256 votePower = governanceToken.balanceOf(msg.sender);
        proposals[proposalIndex].voteCount += votePower;
    }

    // Function to execute a proposal after voting
    function executeProposal(uint256 proposalIndex) public {
        Proposal storage proposal = proposals[proposalIndex];
        require(!proposal.executed, "Proposal already executed");

        proposal.executed = true;
    }
}
