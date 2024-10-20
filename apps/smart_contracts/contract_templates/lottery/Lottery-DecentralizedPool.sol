// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LotteryPool {
    address[] public participants;
    uint256 public poolSize;
    uint256 public maxParticipants;
    bool public poolOpen;

    event PoolOpened(uint256 maxParticipants);
    event ParticipantJoined(address indexed participant);
    event WinnerSelected(address indexed winner, uint256 prizeAmount);

    function openPool(uint256 _maxParticipants) public {
        require(!poolOpen, "Pool already open");

        maxParticipants = _maxParticipants;
        poolOpen = true;

        emit PoolOpened(maxParticipants);
    }

    function joinPool() public payable {
        require(poolOpen, "Pool is not open");
        require(msg.value == 1 ether, "Exact entry fee required");
        require(participants.length < maxParticipants, "Pool is full");

        participants.push(msg.sender);
        poolSize += msg.value;

        emit ParticipantJoined(msg.sender);

        if (participants.length == maxParticipants) {
            selectWinner();
        }
    }

    function selectWinner() private {
        uint256 randomIndex = random() % participants.length;
        address winner = participants[randomIndex];

        payable(winner).transfer(poolSize);

        emit WinnerSelected(winner, poolSize);

        // Reset pool
        poolSize = 0;
        participants = new address ;
        poolOpen = false;
    }

    function random() private view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(block.difficulty, block.timestamp, participants)));
    }
}
