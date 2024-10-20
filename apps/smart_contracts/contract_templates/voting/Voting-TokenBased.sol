// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TokenBasedVoting {
    IERC20 public governanceToken;
    struct Proposal {
        string description;
        uint256 votesFor;
        uint256 votesAgainst;
        bool executed;
    }

    Proposal[] public proposals;

    mapping(address => mapping(uint256 => bool)) public hasVoted;

    event ProposalCreated(uint256 indexed proposalId, string description);
    event Voted(uint256 indexed proposalId, address indexed voter, bool vote);

    constructor(IERC20 _governanceToken) {
        governanceToken = _governanceToken;
    }

    function createProposal(string memory description) public {
        proposals.push(Proposal({
            description: description,
            votesFor: 0,
            votesAgainst: 0,
            executed: false
        }));

        emit ProposalCreated(proposals.length - 1, description);
    }

    function vote(uint256 proposalId, bool voteFor) public {
        require(!hasVoted[msg.sender][proposalId], "Already voted");
        require(proposalId < proposals.length, "Invalid proposal");

        uint256 voterBalance = governanceToken.balanceOf(msg.sender);
        require(voterBalance > 0, "No voting power");

        hasVoted[msg.sender][proposalId] = true;

        if (voteFor) {
            proposals[proposalId].votesFor += voterBalance;
        } else {
            proposals[proposalId].votesAgainst += voterBalance;
        }

        emit Voted(proposalId, msg.sender, voteFor);
    }

    function executeProposal(uint256 proposalId) public {
        require(proposalId < proposals.length, "Invalid proposal");
        require(!proposals[proposalId].executed, "Proposal already executed");

        proposals[proposalId].executed = true;
        // Execute proposal logic here, e.g., upgrade contract, transfer funds, etc.
    }
}
