// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TeamVesting {
    IERC20 public token;
    address public admin;
    uint256 public totalTokens;
    uint256 public releasedTokens;

    struct TeamMember {
        address member;
        uint256 allocation;  // Percentage allocation for this member (e.g., 10% = 1000)
    }

    TeamMember[] public teamMembers;

    uint256 public startTime;
    uint256 public duration;

    constructor(IERC20 _token, address _admin, uint256 _startTime, uint256 _duration, uint256 _totalTokens) {
        token = _token;
        admin = _admin;
        startTime = _startTime;
        duration = _duration;
        totalTokens = _totalTokens;
    }

    function addTeamMember(address member, uint256 allocation) public {
        require(msg.sender == admin, "Only admin can add team members");
        teamMembers.push(TeamMember({
            member: member,
            allocation: allocation
        }));
    }

    function release() public {
        require(block.timestamp >= startTime, "Vesting hasn't started yet");
        uint256 vestedAmount = _vestedAmount();
        uint256 unreleased = vestedAmount - releasedTokens;

        require(unreleased > 0, "No tokens to release");

        for (uint256 i = 0; i < teamMembers.length; i++) {
            uint256 teamShare = (unreleased * teamMembers[i].allocation) / 10000;
            token.transfer(teamMembers[i].member, teamShare);
        }

        releasedTokens += unreleased;
    }

    function _vestedAmount() internal view returns (uint256) {
        if (block.timestamp >= startTime + duration) {
            return totalTokens;
        } else {
            return (totalTokens * (block.timestamp - startTime)) / duration;
        }
    }
}
