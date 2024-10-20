// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TimelockGovernance {
    IERC20 public governanceToken;
    uint256 public timelockDuration;

    struct Proposal {
        string description;
        uint256 voteCount;
        uint256 executionTime;
        bool executed;
    }

    Proposal[] public proposals;

    constructor(IERC20 _governanceToken, uint256 _timelockDuration) {
        governanceToken = _governanceToken;
        timelockDuration = _timelockDuration;
    }

    function createProposal(string memory description) public {
        proposals.push(Proposal({
            description: description,
            voteCount: 0,
            executionTime: block.timestamp + timelockDuration,
            executed: false
        }));
    }

    function vote(uint256 proposalIndex) public {
        require(proposalIndex < proposals.length, "Invalid proposal");

        uint256 votePower = governanceToken.balanceOf(msg.sender);
        proposals[proposalIndex].voteCount += votePower;
    }

    function executeProposal(uint256 proposalIndex) public {
        require(proposalIndex < proposals.length, "Invalid proposal");
        require(!proposals[proposalIndex].executed, "Proposal already executed");
        require(block.timestamp >= proposals[proposalIndex].executionTime, "Timelock not expired");

        proposals[proposalIndex].executed = true;
    }
}
