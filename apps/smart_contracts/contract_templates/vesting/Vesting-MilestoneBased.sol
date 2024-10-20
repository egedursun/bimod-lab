// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract MilestoneVesting {
    IERC20 public token;
    address public beneficiary;

    struct Milestone {
        string description;
        uint256 releaseAmount;
        bool released;
    }

    Milestone[] public milestones;

    constructor(IERC20 _token, address _beneficiary, Milestone[] memory _milestones) {
        token = _token;
        beneficiary = _beneficiary;

        for (uint256 i = 0; i < _milestones.length; i++) {
            milestones.push(_milestones[i]);
        }
    }

    function release(uint256 milestoneIndex) public {
        require(milestoneIndex < milestones.length, "Invalid milestone index");
        Milestone storage milestone = milestones[milestoneIndex];

        require(!milestone.released, "Milestone already released");

        milestone.released = true;
        token.transfer(beneficiary, milestone.releaseAmount);
    }
}
