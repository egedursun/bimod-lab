// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract QuadraticVoting {
    struct Proposal {
        string description;
        uint256 totalVotes;
        uint256 totalCost;
    }

    mapping(uint256 => mapping(address => uint256)) public votes;
    mapping(uint256 => Proposal) public proposals;

    event ProposalCreated(uint256 indexed proposalId, string description);
    event Voted(uint256 indexed proposalId, address indexed voter, uint256 votes);

    function createProposal(string memory description) public {
        proposals[uint256(keccak256(abi.encodePacked(description, block.timestamp)))] = Proposal({
            description: description,
            totalVotes: 0,
            totalCost: 0
        });

        emit ProposalCreated(uint256(keccak256(abi.encodePacked(description, block.timestamp))), description);
    }

    function vote(uint256 proposalId, uint256 votesToBuy) public payable {
        require(msg.value >= (votesToBuy ** 2), "Not enough funds for votes");

        votes[proposalId][msg.sender] += votesToBuy;
        proposals[proposalId].totalVotes += votesToBuy;
        proposals[proposalId].totalCost += msg.value;

        emit Voted(proposalId, msg.sender, votesToBuy);
    }
}
