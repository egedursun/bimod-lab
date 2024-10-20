// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DAOTreasury {
    address public owner;
    mapping(address => bool) public members;
    mapping(address => uint256) public treasuryBalances;
    uint256 public proposalIndex;

    struct Proposal {
        address payable recipient;
        uint256 amount;
        uint256 voteCount;
        bool executed;
    }

    Proposal[] public proposals;
    mapping(uint256 => mapping(address => bool)) public hasVoted;

    constructor() {
        owner = msg.sender;
    }

    function deposit() public payable {
        treasuryBalances[msg.sender] += msg.value;
    }

    function createProposal(address payable recipient, uint256 amount) public {
        require(members[msg.sender], "Not a DAO member");

        proposals.push(Proposal({
            recipient: recipient,
            amount: amount,
            voteCount: 0,
            executed: false
        }));
    }

    function vote(uint256 proposalId) public {
        require(members[msg.sender], "Not a DAO member");
        require(!hasVoted[proposalId][msg.sender], "Already voted");
        require(!proposals[proposalId].executed, "Proposal already executed");

        proposals[proposalId].voteCount++;
        hasVoted[proposalId][msg.sender] = true;
    }

    function executeProposal(uint256 proposalId) public {
        Proposal storage proposal = proposals[proposalId];
        require(proposal.voteCount > 0, "Not enough votes");
        require(!proposal.executed, "Proposal already executed");

        proposal.executed = true;
        proposal.recipient.transfer(proposal.amount);
    }
}
