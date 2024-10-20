// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleLottery {
    address public owner;
    address[] public participants;
    uint256 public ticketPrice;
    bool public lotteryOpen;

    event LotteryStarted(uint256 ticketPrice);
    event TicketPurchased(address indexed buyer);
    event WinnerPicked(address indexed winner, uint256 prizeAmount);

    constructor() {
        owner = msg.sender;
    }

    function startLottery(uint256 _ticketPrice) public {
        require(msg.sender == owner, "Only owner can start the lottery");
        require(!lotteryOpen, "Lottery already open");

        ticketPrice = _ticketPrice;
        lotteryOpen = true;

        emit LotteryStarted(ticketPrice);
    }

    function buyTicket() public payable {
        require(lotteryOpen, "Lottery is not open");
        require(msg.value == ticketPrice, "Incorrect ticket price");

        participants.push(msg.sender);

        emit TicketPurchased(msg.sender);
    }

    function pickWinner() public {
        require(msg.sender == owner, "Only owner can pick the winner");
        require(lotteryOpen, "Lottery is not open");
        require(participants.length > 0, "No participants in the lottery");

        // Randomly pick a winner
        uint256 randomIndex = random() % participants.length;
        address winner = participants[randomIndex];
        uint256 prizeAmount = address(this).balance;

        // Transfer the prize to the winner
        payable(winner).transfer(prizeAmount);

        // Reset the lottery
        participants = new address ;
        lotteryOpen = false;

        emit WinnerPicked(winner, prizeAmount);
    }

    function random() private view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(block.difficulty, block.timestamp, participants)));
    }

    function getParticipants() public view returns (address[] memory) {
        return participants;
    }
}
