// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract CustomVesting {
    IERC20 public token;
    address public admin;

    struct VestingSchedule {
        address beneficiary;
        uint256 startTime;
        uint256 duration;
        uint256 totalTokens;
        uint256 releasedTokens;
    }

    mapping(address => VestingSchedule) public schedules;

    constructor(IERC20 _token, address _admin) {
        token = _token;
        admin = _admin;
    }

    function setVestingSchedule(
        address beneficiary,
        uint256 startTime,
        uint256 duration,
        uint256 totalTokens
    ) public {
        require(msg.sender == admin, "Only admin can set vesting schedules");

        schedules[beneficiary] = VestingSchedule({
            beneficiary: beneficiary,
            startTime: startTime,
            duration: duration,
            totalTokens: totalTokens,
            releasedTokens: 0
        });
    }

    function release(address beneficiary) public {
        VestingSchedule storage schedule = schedules[beneficiary];
        require(block.timestamp >= schedule.startTime, "Vesting hasn't started yet");

        uint256 vestedAmount = _vestedAmount(beneficiary);
        uint256 unreleased = vestedAmount - schedule.releasedTokens;

        require(unreleased > 0, "No tokens to release");

        schedule.releasedTokens += unreleased;
        token.transfer(beneficiary, unreleased);
    }

    function _vestedAmount(address beneficiary) internal view returns (uint256) {
        VestingSchedule storage schedule = schedules[beneficiary];
        if (block.timestamp >= schedule.startTime + schedule.duration) {
            return schedule.totalTokens;
        } else {
            return (schedule.totalTokens * (block.timestamp - schedule.startTime)) / schedule.duration;
        }
    }
}
