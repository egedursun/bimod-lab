// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RandomnessOracle {
    address public admin;
    mapping(address => bool) public trustedSources;
    uint256 public latestRandomNumber;

    event RandomNumberUpdated(uint256 randomNumber);

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

    function updateRandomNumber(uint256 randomNumber) public {
        require(trustedSources[msg.sender], "Not a trusted source");

        latestRandomNumber = randomNumber;
        emit RandomNumberUpdated(randomNumber);
    }

    function getRandomNumber() public view returns (uint256) {
        return latestRandomNumber;
    }
}
