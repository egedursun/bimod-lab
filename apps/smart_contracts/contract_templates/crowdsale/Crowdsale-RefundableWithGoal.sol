// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract GoalBasedRefundableCrowdsale {
    IERC20 public token;
    address payable public wallet;
    uint256 public rate;
    uint256 public weiRaised;
    uint256 public goal;
    bool public goalReached;
    mapping(address => uint256) public contributions;

    constructor(
        uint256 _rate,
        address payable _wallet,
        IERC20 _token,
        uint256 _goal
    ) {
        require(_rate > 0, "Rate must be greater than 0");
        require(_goal > 0, "Goal must be greater than 0");
        require(_wallet != address(0), "Invalid wallet address");
        require(address(_token) != address(0), "Invalid token address");

        rate = _rate;
        wallet = _wallet;
        token = _token;
        goal = _goal;
    }

    function buyTokens() public payable {
        uint256 weiAmount = msg.value;
        require(weiAmount > 0, "Ether amount is 0");

        uint256 tokens = weiAmount * rate;
        contributions[msg.sender] += weiAmount;
        weiRaised += weiAmount;
        token.transfer(msg.sender, tokens);

        if (weiRaised >= goal) {
            goalReached = true;
            wallet.transfer(weiRaised);  // Forward funds to the wallet once goal is reached
        }
    }

    function claimRefund() public {
        require(!goalReached, "Goal reached, refunds unavailable");
        uint256 contribution = contributions[msg.sender];
        require(contribution > 0, "No contribution found");

        contributions[msg.sender] = 0;
        payable(msg.sender).transfer(contribution);  // Refund contributions
    }
}
