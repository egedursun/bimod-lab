// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TimedCrowdsale {
    IERC20 public token;
    address payable public wallet;
    uint256 public rate;
    uint256 public weiRaised;
    uint256 public openingTime;
    uint256 public closingTime;

    constructor(
        uint256 _rate,
        address payable _wallet,
        IERC20 _token,
        uint256 _openingTime,
        uint256 _closingTime
    ) {
        require(_rate > 0, "Rate must be greater than 0");
        require(_wallet != address(0), "Invalid wallet address");
        require(address(_token) != address(0), "Invalid token address");
        require(_openingTime < _closingTime, "Opening time must be before closing time");

        rate = _rate;
        wallet = _wallet;
        token = _token;
        openingTime = _openingTime;
        closingTime = _closingTime;
    }

    modifier onlyWhileOpen() {
        require(block.timestamp >= openingTime && block.timestamp <= closingTime, "Crowdsale is not open");
        _;
    }

    function buyTokens() public payable onlyWhileOpen {
        uint256 weiAmount = msg.value;
        uint256 tokens = weiAmount * rate;

        weiRaised += weiAmount;
        token.transfer(msg.sender, tokens);
        wallet.transfer(weiAmount);
    }

    function hasClosed() public view returns (bool) {
        return block.timestamp > closingTime;
    }
}
