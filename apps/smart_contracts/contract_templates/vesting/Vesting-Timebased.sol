// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TimeBasedVesting {
    IERC20 public token;
    address public beneficiary;
    uint256 public startTime;
    uint256 public duration;

    uint256 public totalTokens;
    uint256 public releasedTokens;

    constructor(IERC20 _token, address _beneficiary, uint256 _startTime, uint256 _duration, uint256 _totalTokens) {
        token = _token;
        beneficiary = _beneficiary;
        startTime = _startTime;
        duration = _duration;
        totalTokens = _totalTokens;
    }

    function release() public {
        require(block.timestamp >= startTime, "Vesting hasn't started yet");

        uint256 vestedAmount = _vestedAmount();
        uint256 unreleased = vestedAmount - releasedTokens;

        require(unreleased > 0, "No tokens to release");

        releasedTokens += unreleased;
        token.transfer(beneficiary, unreleased);
    }

    function _vestedAmount() internal view returns (uint256) {
        if (block.timestamp >= startTime + duration) {
            return totalTokens;
        } else {
            return (totalTokens * (block.timestamp - startTime)) / duration;
        }
    }
}
