// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RaffleLottery {
    address public owner;
    address[] public tickets;
    uint256 public ticketPrice;
    bool public lotteryOpen;

    event LotteryStarted(uint256 ticketPrice);
    event TicketPurchased(address indexed buyer, uint256 ticketCount);
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

    function buyTickets(uint256 ticketCount) public payable {
        require(lotteryOpen, "Lottery is not open");
        require(msg.value == ticketCount * ticketPrice, "Incorrect amount");

        for (uint256 i = 0; i < ticketCount; i++) {
            tickets.push(msg.sender);
        }

        emit TicketPurchased(msg.sender, ticketCount);
    }

    function pickWinner() public {
        require(msg.sender == owner, "Only owner can pick the winner");
        require(lotteryOpen, "Lottery is not open");
        require(tickets.length > 0, "No tickets sold");

        uint256 randomIndex = random() % tickets.length;
        address winner = tickets[randomIndex];
        uint256 prizeAmount = address(this).balance;

        payable(winner).transfer(prizeAmount);

        // Reset the lottery
        tickets = new address ;
        lotteryOpen = false;

        emit WinnerPicked(winner, prizeAmount);
    }

    function random() private view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(block.difficulty, block.timestamp, tickets)));
    }

    function getTickets() public view returns (address[] memory) {
        return tickets;
    }
}
