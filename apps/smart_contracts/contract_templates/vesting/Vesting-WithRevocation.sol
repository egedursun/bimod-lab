// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract RevocableVesting {
    IERC20 public token;
    address public beneficiary;
    address public admin;
    uint256 public startTime;
    uint256 public duration;
    bool public revoked;

    uint256 public totalTokens;
    uint256 public releasedTokens;

    constructor(IERC20 _token, address _beneficiary, address _admin, uint256 _startTime, uint256 _duration, uint256 _totalTokens) {
        token = _token;
        beneficiary = _beneficiary;
        admin = _admin;
        startTime = _startTime;
        duration = _duration;
        totalTokens = _totalTokens;
    }

    function release() public {
        require(!revoked, "Vesting has been revoked");
        require(block.timestamp >= startTime, "Vesting hasn't started yet");

        uint256 vestedAmount = _vestedAmount();
        uint256 unreleased = vestedAmount - releasedTokens;

        require(unreleased > 0, "No tokens to release");

        releasedTokens += unreleased;
        token.transfer(beneficiary, unreleased);
    }

    function revoke() public {
        require(msg.sender == admin, "Only admin can revoke vesting");
        revoked = true;
    }

    function _vestedAmount() internal view returns (uint256) {
        if (revoked) {
            return releasedTokens;
        } else if (block.timestamp >= startTime + duration) {
            return totalTokens;
        } else {
            return (totalTokens * (block.timestamp - startTime)) / duration;
        }
    }
}
