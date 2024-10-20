// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract PerformanceVesting {
    IERC20 public token;
    address public beneficiary;
    address public admin;
    uint256 public totalTokens;
    uint256 public releasedTokens;

    struct PerformanceCondition {
        string description;
        bool isMet;
        uint256 releaseAmount;
    }

    PerformanceCondition[] public conditions;

    constructor(IERC20 _token, address _beneficiary, address _admin, uint256 _totalTokens) {
        token = _token;
        beneficiary = _beneficiary;
        admin = _admin;
        totalTokens = _totalTokens;
    }

    function addCondition(string memory description, uint256 releaseAmount) public {
        require(msg.sender == admin, "Only admin can add conditions");
        conditions.push(PerformanceCondition({
            description: description,
            isMet: false,
            releaseAmount: releaseAmount
        }));
    }

    function meetCondition(uint256 conditionIndex) public {
        require(msg.sender == admin, "Only admin can mark conditions as met");
        require(!conditions[conditionIndex].isMet, "Condition already met");

        conditions[conditionIndex].isMet = true;
    }

    function release() public {
        uint256 unreleasedTokens = 0;
        for (uint256 i = 0; i < conditions.length; i++) {
            if (conditions[i].isMet) {
                unreleasedTokens += conditions[i].releaseAmount;
            }
        }
        unreleasedTokens -= releasedTokens;
        require(unreleasedTokens > 0, "No tokens to release");

        releasedTokens += unreleasedTokens;
        token.transfer(beneficiary, unreleasedTokens);
    }
}
