// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MultiWinnerLottery {
    address public owner;
    address[] public participants;
    uint256 public ticketPrice;
    uint256 public numberOfWinners;
    bool public lotteryOpen;

    event LotteryStarted(uint256 ticketPrice, uint256 numberOfWinners);
    event TicketPurchased(address indexed buyer);
    event WinnersPicked(address[] winners, uint256 prizeAmount);

    constructor() {
        owner = msg.sender;
    }

    function startLottery(uint256 _ticketPrice, uint256 _numberOfWinners) public {
        require(msg.sender == owner, "Only owner can start the lottery");
        require(!lotteryOpen, "Lottery already open");
        require(_numberOfWinners > 0, "Must have at least one winner");

        ticketPrice = _ticketPrice;
        numberOfWinners = _numberOfWinners;
        lotteryOpen = true;

        emit LotteryStarted(ticketPrice, numberOfWinners);
    }

    function buyTicket() public payable {
        require(lotteryOpen, "Lottery is not open");
        require(msg.value == ticketPrice, "Incorrect ticket price");

        participants.push(msg.sender);

        emit TicketPurchased(msg.sender);
    }

    function pickWinners() public {
        require(msg.sender == owner, "Only owner can pick winners");
        require(participants.length >= numberOfWinners, "Not enough participants");

        address[] memory winners = new address[](numberOfWinners);
        uint256 prizeAmount = address(this).balance / numberOfWinners;

        for (uint256 i = 0; i < numberOfWinners; i++) {
            uint256 randomIndex = random() % participants.length;
            winners[i] = participants[randomIndex];
            payable(winners[i]).transfer(prizeAmount);
        }

        // Reset the lottery
        participants = new address ;
        lotteryOpen = false;

        emit WinnersPicked(winners, prizeAmount);
    }

    function random() private view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(block.difficulty, block.timestamp, participants)));
    }
}
