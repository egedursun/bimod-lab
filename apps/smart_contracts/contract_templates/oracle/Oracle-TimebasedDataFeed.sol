// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TimeBasedOracle {
    address public admin;
    uint256 public latestData;
    uint256 public lastUpdated;
    uint256 public updateInterval;  // Time in seconds

    event DataUpdated(uint256 data, uint256 timestamp);

    constructor(uint256 _updateInterval) {
        admin = msg.sender;
        updateInterval = _updateInterval;
        lastUpdated = block.timestamp;
    }

    function updateData(uint256 data) public {
        require(block.timestamp >= lastUpdated + updateInterval, "Update interval not reached");
        latestData = data;
        lastUpdated = block.timestamp;

        emit DataUpdated(data, lastUpdated);
    }

    function getData() public view returns (uint256) {
        require(block.timestamp <= lastUpdated + updateInterval, "Data is outdated");
        return latestData;
    }
}
