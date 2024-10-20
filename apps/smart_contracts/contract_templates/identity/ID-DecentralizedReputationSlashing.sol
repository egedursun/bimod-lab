// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ReputationSlashing {
    mapping(address => uint256) public reputations;
    mapping(address => uint256) public slashes;

    event ReputationSlashed(address indexed user, uint256 amount, string reason);

    function slashReputation(address user, uint256 amount, string memory reason) public {
        require(reputations[user] >= amount, "Cannot slash more than available reputation");

        reputations[user] -= amount;
        slashes[user] += amount;

        emit ReputationSlashed(user, amount, reason);
    }

    function getReputation(address user) public view returns (uint256) {
        return reputations[user];
    }

    function getSlashedAmount(address user) public view returns (uint256) {
        return slashes[user];
    }
}
