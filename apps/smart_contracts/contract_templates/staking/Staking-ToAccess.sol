// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract StakeToAccess {
    IERC20 public accessToken;
    uint256 public requiredStake;

    mapping(address => uint256) public stakedBalances;

    constructor(IERC20 _accessToken, uint256 _requiredStake) {
        accessToken = _accessToken;
        requiredStake = _requiredStake;
    }

    function stake() public {
        require(stakedBalances[msg.sender] == 0, "Already staked");

        accessToken.transferFrom(msg.sender, address(this), requiredStake);
        stakedBalances[msg.sender] = requiredStake;
    }

    function withdraw() public {
        require(stakedBalances[msg.sender] > 0, "No staked balance");

        uint256 amount = stakedBalances[msg.sender];
        stakedBalances[msg.sender] = 0;
        accessToken.transfer(msg.sender, amount);
    }

    function hasAccess(address user) public view returns (bool) {
        return stakedBalances[user] >= requiredStake;
    }
}
