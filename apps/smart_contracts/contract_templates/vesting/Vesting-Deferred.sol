// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract DeferredVesting {
    IERC20 public token;
    address public beneficiary;
    uint256 public deferredTime;
    uint256 public totalTokens;
    bool public released;

    constructor(IERC20 _token, address _beneficiary, uint256 _deferredTime, uint256 _totalTokens) {
        token = _token;
        beneficiary = _beneficiary;
        deferredTime = _deferredTime;
        totalTokens = _totalTokens;
        released = false;
    }

    function release() public {
        require(block.timestamp >= deferredTime, "Deferred period not yet completed");
        require(!released, "Tokens already released");

        released = true;
        token.transfer(beneficiary, totalTokens);
    }
}
