// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract StakedGovernance {
    IERC20 public governanceToken;
    uint256 public stakeAmount;

    struct Proposal {
        string description;
        uint256 voteCount;
        uint256 stakeAmount;
        bool executed;
    }

    Proposal[] public proposals;
    mapping(address => uint256) public stakes;

    constructor(IERC20 _governanceToken, uint256 _stakeAmount) {
        governanceToken = _governanceToken;
        stakeAmount = _stakeAmount;
    }

    function createProposal(string memory description) public {
        require(governanceToken.balanceOf(msg.sender) >= stakeAmount, "Insufficient stake");

        governanceToken.transferFrom(msg.sender, address(this), stakeAmount);

        proposals.push(Proposal({
            description: description,
            voteCount: 0,
            stakeAmount: stakeAmount,
            executed: false
        }));
    }

    function vote(uint256 proposalIndex) public {
        require(proposalIndex < proposals.length, "Invalid proposal");
        require(governanceToken.balanceOf(msg.sender) >= stakeAmount, "Insufficient stake");

        governanceToken.transferFrom(msg.sender, address(this), stakeAmount);
        stakes[msg.sender] += stakeAmount;

        proposals[proposalIndex].voteCount += governanceToken.balanceOf(msg.sender);
    }

    function executeProposal(uint256 proposalIndex) public {
        require(proposalIndex < proposals.length, "Invalid proposal");
        Proposal storage proposal = proposals[proposalIndex];
        require(!proposal.executed, "Proposal already executed");

        if (proposal.voteCount > 0) {
            proposal.executed = true;
            governanceToken.transfer(msg.sender, proposal.stakeAmount);  // Return stake if successful
        }
    }

    function penalizeFailedProposal(uint256 proposalIndex) public {
        require(proposalIndex < proposals.length, "Invalid proposal");
        Proposal storage proposal = proposals[proposalIndex];
        require(!proposal.executed, "Proposal already executed");

        // Penalize (burn or send to treasury)
        proposal.executed = true;
        governanceToken.transfer(address(0), proposal.stakeAmount);  // Burn stake if unsuccessful
    }
}
