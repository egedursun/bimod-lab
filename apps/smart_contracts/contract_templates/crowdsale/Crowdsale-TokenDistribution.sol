// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract TokenDistributionCrowdsale is Ownable {
    IERC20 public token;
    address payable public wallet;
    uint256 public rate;
    uint256 public weiRaised;
    uint256 public closingTime;
    bool public isFinalized;
    mapping(address => uint256) public contributions;

    constructor(
        uint256 _rate,
        address payable _wallet,
        IERC20 _token,
        uint256 _closingTime
    ) {
        require(_rate > 0, "Rate must be greater than 0");
        require(_closingTime > block.timestamp, "Closing time is in the past");
        require(_wallet != address(0), "Invalid wallet address");
        require(address(_token) != address(0), "Invalid token address");

        rate = _rate;
        wallet = _wallet;
        token = _token;
        closingTime = _closingTime;
    }

    modifier onlyWhileOpen() {
        require(block.timestamp <= closingTime, "Crowdsale is closed");
        _;
    }

    function buyTokens() public payable onlyWhileOpen {
        uint256 weiAmount = msg.value;
        require(weiAmount > 0, "Ether amount is 0");

        contributions[msg.sender] += weiAmount;
        weiRaised += weiAmount;

        wallet.transfer(weiAmount);  // Forward Ether to the wallet
    }

    function finalize() public onlyOwner {
        require(!isFinalized, "Crowdsale already finalized");
        require(block.timestamp > closingTime, "Crowdsale is still open");

        isFinalized = true;
        uint256 totalTokens = token.balanceOf(address(this));
        for (uint256 i = 0; i < totalTokens; i++) {
            address contributor = payable(msg.sender); // Replace with actual contributor data logic
            uint256 tokensOwed = contributions[contributor] * rate;
            token.transfer(contributor, tokensOwed);
        }
    }
}
