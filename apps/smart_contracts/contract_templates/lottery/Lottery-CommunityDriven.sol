// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CommunityLottery {
    address public owner;
    address[] public participants;
    uint256 public ticketPrice;
    bool public lotteryOpen;

    mapping(address => bool) public votes;
    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;

    struct Proposal {
        uint256 id;
        string description;
        uint256 voteCount;
        bool executed;
    }

    event LotteryStarted(uint256 ticketPrice);
    event ProposalCreated(uint256 id, string description);
    event ProposalVoted(uint256 id, address voter);
    event ProposalExecuted(uint256 id);

    constructor(uint256 _ticketPrice) {
        owner = msg.sender;
        ticketPrice = _ticketPrice;
        lotteryOpen = true;
    }

    function createProposal(string memory description) public {
        proposals[proposalCount] = Proposal({
            id: proposalCount,
            description: description,
            voteCount: 0,
            executed: false
        });

        emit ProposalCreated(proposalCount, description);
        proposalCount++;
    }

    function voteOnProposal(uint256 proposalId) public {
        require(!votes[msg.sender], "Already voted");

        proposals[proposalId].voteCount++;
        votes[msg.sender] = true;

        emit ProposalVoted(proposalId, msg.sender);
    }

    function executeProposal(uint256 proposalId) public {
        Proposal storage proposal = proposals[proposalId];
        require(!proposal.executed, "Proposal already executed");
        require(proposal.voteCount > (participants.length / 2), "Not enough votes");

        // Execute the proposal logic
        proposal.executed = true;

        emit ProposalExecuted(proposalId);
    }

    function buyTicket() public payable {
        require(lotteryOpen, "Lottery is not open");
        require(msg.value == ticketPrice, "Incorrect ticket price");

        participants.push(msg.sender);
    }

    function pickWinner() public {
        require(msg.sender == owner, "Only owner can pick the winner");
        require(participants.length > 0, "No participants");

        uint256 randomIndex = random() % participants.length;
        address winner = participants[randomIndex];
        uint256 prizeAmount = address(this).balance;

        payable(winner).transfer(prizeAmount);

        participants = new address;
        lotteryOpen = false;
    }

    function random() private view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(block.difficulty, block.timestamp, participants)));
    }
}
