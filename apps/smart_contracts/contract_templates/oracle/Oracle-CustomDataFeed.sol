// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CustomDataFeedOracle {
    address public admin;
    mapping(address => bool) public trustedSources;
    string public latestData;

    event DataUpdated(string data);

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

    function updateData(string memory data) public {
        require(trustedSources[msg.sender], "Not a trusted source");

        latestData = data;
        emit DataUpdated(data);
    }

    function getData() public view returns (string memory) {
        return latestData;
    }
}
