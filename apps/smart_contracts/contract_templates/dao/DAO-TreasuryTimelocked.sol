// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TimelockDAO {
    address public owner;
    uint256 public timelockDuration;

    struct Proposal {
        address payable recipient;
        uint256 amount;
        uint256 voteCount;
        uint256 executionTime;
        bool executed;
    }

    Proposal[] public proposals;

    constructor(uint256 _timelockDuration) {
        owner = msg.sender;
        timelockDuration = _timelockDuration;
    }

    function createProposal(address payable recipient, uint256 amount) public {
        proposals.push(Proposal({
            recipient: recipient,
            amount: amount,
            voteCount: 0,
            executionTime: block.timestamp + timelockDuration,
            executed: false
        }));
    }

    function vote(uint256 proposalIndex) public {
        require(proposalIndex < proposals.length, "Invalid proposal");
        proposals[proposalIndex].voteCount++;
    }

    function executeProposal(uint256 proposalIndex) public {
        Proposal storage proposal = proposals[proposalIndex];
        require(block.timestamp >= proposal.executionTime, "Timelock not expired");
        require(!proposal.executed, "Proposal already executed");

        proposal.executed = true;
        proposal.recipient.transfer(proposal.amount);
    }
}
