// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MultiSourceOracle {
    address public admin;
    mapping(address => bool) public trustedSources;
    mapping(address => uint256) public latestValues;
    uint256 public aggregationResult;

    event ValueUpdated(address indexed source, uint256 value);
    event AggregationCompleted(uint256 result);

    constructor() {
        admin = msg.sender;
    }

    function addTrustedSource(address source) public {
        require(msg.sender == admin, "Only admin can add sources");
        trustedSources[source] = true;
    }

    function removeTrustedSource(address source) public {
        require(msg.sender == admin, "Only admin can remove sources");
        trustedSources[source] = false;
    }

    function updateValue(uint256 value) public {
        require(trustedSources[msg.sender], "Not a trusted source");

        latestValues[msg.sender] = value;
        emit ValueUpdated(msg.sender, value);
    }

    function aggregateValues() public {
        uint256 totalValue;
        uint256 sourceCount;

        for (uint256 i = 0; i < address(this).balance; i++) {
            if (trustedSources[msg.sender]) {
                totalValue += latestValues[msg.sender];
                sourceCount++;
            }
        }

        aggregationResult = totalValue / sourceCount;
        emit AggregationCompleted(aggregationResult);
    }

    function getAggregatedResult() public view returns (uint256) {
        return aggregationResult;
    }
}
