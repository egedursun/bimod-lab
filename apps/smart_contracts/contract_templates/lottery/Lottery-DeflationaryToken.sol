// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract DeflationaryTokenLottery {
    IERC20 public token;
    address public owner;
    address[] public participants;
    uint256 public ticketPrice;
    uint256 public burnPercentage;
    bool public lotteryOpen;

    event LotteryStarted(uint256 ticketPrice);
    event TicketPurchased(address indexed buyer);
    event WinnerPicked(address indexed winner, uint256 prizeAmount);

    constructor(IERC20 _token, uint256 _ticketPrice, uint256 _burnPercentage) {
        owner = msg.sender;
        token = _token;
        ticketPrice = _ticketPrice;
        burnPercentage = _burnPercentage;
    }

    function startLottery() public {
        require(msg.sender == owner, "Only owner can start the lottery");
        require(!lotteryOpen, "Lottery already open");

        lotteryOpen = true;
        emit LotteryStarted(ticketPrice);
    }

    function buyTicket() public {
        require(lotteryOpen, "Lottery is not open");
        require(token.balanceOf(msg.sender) >= ticketPrice, "Insufficient balance");

        uint256 burnAmount = (ticketPrice * burnPercentage) / 100;
        uint256 prizeAmount = ticketPrice - burnAmount;

        // Burn a portion of the tokens
        token.transferFrom(msg.sender, address(0), burnAmount);

        // Add the remaining portion to the prize pool
        token.transferFrom(msg.sender, address(this), prizeAmount);

        participants.push(msg.sender);

        emit TicketPurchased(msg.sender);
    }

    function pickWinner() public {
        require(msg.sender == owner, "Only owner can pick the winner");
        require(participants.length > 0, "No participants");

        uint256 randomIndex = random() % participants.length;
        address winner = participants[randomIndex];
        uint256 prizeAmount = token.balanceOf(address(this));

        token.transfer(winner, prizeAmount);

        participants = new address ;
        lotteryOpen = false;

        emit WinnerPicked(winner, prizeAmount);
    }

    function random() private view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(block.difficulty, block.timestamp, participants)));
    }
}
