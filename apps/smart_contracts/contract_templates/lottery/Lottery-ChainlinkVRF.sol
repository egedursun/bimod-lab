// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract ChainlinkVRFLottery is VRFConsumerBaseV2 {
    address public owner;
    address[] public participants;
    uint256 public ticketPrice;
    uint64 public subscriptionId;
    bytes32 public keyHash;
    VRFCoordinatorV2Interface COORDINATOR;

    uint256 public requestId;
    bool public lotteryOpen;

    event LotteryStarted(uint256 ticketPrice);
    event TicketPurchased(address indexed buyer);
    event WinnerPicked(address indexed winner, uint256 prizeAmount);

    constructor(
        address vrfCoordinator,
        uint64 _subscriptionId,
        bytes32 _keyHash
    ) VRFConsumerBaseV2(vrfCoordinator) {
        owner = msg.sender;
        COORDINATOR = VRFCoordinatorV2Interface(vrfCoordinator);
        subscriptionId = _subscriptionId;
        keyHash = _keyHash;
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

        // Request randomness from Chainlink VRF
        requestId = COORDINATOR.requestRandomWords(keyHash, subscriptionId, 3, 200000, 1);
    }

    function fulfillRandomWords(uint256, uint256[] memory randomWords) internal override {
        uint256 randomIndex = randomWords[0] % participants.length;
        address winner = participants[randomIndex];
        uint256 prizeAmount = address(this).balance;

        // Transfer the prize to the winner
        payable(winner).transfer(prizeAmount);

        // Reset the lottery
        participants = new address ;
        lotteryOpen = false;

        emit WinnerPicked(winner, prizeAmount);
    }

    function getParticipants() public view returns (address[] memory) {
        return participants;
    }
}
