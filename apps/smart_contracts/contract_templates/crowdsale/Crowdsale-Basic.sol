// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract BasicCrowdsale {
    IERC20 public token;
    address payable public wallet;
    uint256 public rate;  // How many tokens a buyer gets per 1 ether
    uint256 public weiRaised;

    constructor(uint256 _rate, address payable _wallet, IERC20 _token) {
        require(_rate > 0, "Rate must be greater than 0");
        require(_wallet != address(0), "Invalid wallet address");
        require(address(_token) != address(0), "Invalid token address");

        rate = _rate;
        wallet = _wallet;
        token = _token;
    }

    function buyTokens() public payable {
        uint256 weiAmount = msg.value;
        require(weiAmount > 0, "Ether amount is 0");

        uint256 tokens = weiAmount * rate;
        weiRaised += weiAmount;

        token.transfer(msg.sender, tokens);
        wallet.transfer(msg.value);  // Forward Ether to the wallet
    }
}
