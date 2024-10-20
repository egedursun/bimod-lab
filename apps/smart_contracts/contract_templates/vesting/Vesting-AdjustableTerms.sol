// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract AdjustableVesting {
    IERC20 public token;
    address public admin;
    address public beneficiary;
    uint256 public startTime;
    uint256 public duration;
    uint256 public totalTokens;
    uint256 public releasedTokens;

    constructor(IERC20 _token, address _beneficiary, address _admin, uint256 _startTime, uint256 _duration, uint256 _totalTokens) {
        token = _token;
        beneficiary = _beneficiary;
        admin = _admin;
        startTime = _startTime;
        duration = _duration;
        totalTokens = _totalTokens;
        releasedTokens = 0;
    }

    // Allows the admin to adjust vesting terms after initialization
    function adjustVestingTerms(uint256 newDuration, uint256 newTotalTokens) public {
        require(msg.sender == admin, "Only admin can adjust vesting terms");

        duration = newDuration;
        totalTokens = newTotalTokens;
    }

    // Releases vested tokens based on the adjusted terms
    function release() public {
        require(block.timestamp >= startTime, "Vesting hasn't started yet");

        uint256 vestedAmount = _vestedAmount();
        uint256 unreleased = vestedAmount - releasedTokens;

        require(unreleased > 0, "No tokens to release");

        releasedTokens += unreleased;
        token.transfer(beneficiary, unreleased);
    }

    // Internal function to calculate the vested amount
    function _vestedAmount() internal view returns (uint256) {
        if (block.timestamp >= startTime + duration) {
            return totalTokens;
        } else {
            return (totalTokens * (block.timestamp - startTime)) / duration;
        }
    }
}
