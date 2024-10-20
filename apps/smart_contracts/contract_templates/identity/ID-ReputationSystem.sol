// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ReputationSystem {
    mapping(address => uint256) public reputations;

    event ReputationUpdated(address indexed user, uint256 newReputation);

    function increaseReputation(address user, uint256 amount) public {
        reputations[user] += amount;

        emit ReputationUpdated(user, reputations[user]);
    }

    function decreaseReputation(address user, uint256 amount) public {
        require(reputations[user] >= amount, "Reputation cannot go negative");

        reputations[user] -= amount;

        emit ReputationUpdated(user, reputations[user]);
    }

    function getReputation(address user) public view returns (uint256) {
        return reputations[user];
    }
}
