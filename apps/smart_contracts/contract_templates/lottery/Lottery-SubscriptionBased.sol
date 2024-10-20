// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SubscriptionLottery {
    address public owner;
    mapping(address => uint256) public subscriptions;
    uint256 public subscriptionFee;
    uint256 public drawInterval;
    uint256 public lastDrawTime;
    address[] public participants;

    event LotterySubscribed(address indexed participant);
    event WinnerPicked(address indexed winner, uint256 prizeAmount);

    constructor(uint256 _subscriptionFee, uint256 _drawInterval) {
        owner = msg.sender;
        subscriptionFee = _subscriptionFee;
        drawInterval = _drawInterval;
    }

    function subscribe() public payable {
        require(msg.value == subscriptionFee, "Incorrect subscription fee");

        if (subscriptions[msg.sender] == 0) {
            participants.push(msg.sender);
        }

        subscriptions[msg.sender] = block.timestamp;

        emit LotterySubscribed(msg.sender);
    }

    function pickWinner() public {
        require(block.timestamp >= lastDrawTime + drawInterval, "Cannot draw yet");
        require(participants.length > 0, "No participants");

        uint256 randomIndex = random() % participants.length;
        address winner = participants[randomIndex];
        uint256 prizeAmount = address(this).balance;

        payable(winner).transfer(prizeAmount);

        lastDrawTime = block.timestamp;

        emit WinnerPicked(winner, prizeAmount);
    }

    function random() private view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(block.difficulty, block.timestamp, participants)));
    }

    function getParticipants() public view returns (address[] memory) {
        return participants;
    }

    function getSubscriptionStatus(address participant) public view returns (uint256) {
        return subscriptions[participant];
    }
}
