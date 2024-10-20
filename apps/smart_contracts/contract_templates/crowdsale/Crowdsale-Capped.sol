// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract CappedCrowdsale {
    IERC20 public token;
    address payable public wallet;
    uint256 public rate;
    uint256 public weiRaised;
    uint256 public cap;  // Maximum amount of Ether that can be raised

    constructor(
        uint256 _rate,
        address payable _wallet,
        IERC20 _token,
        uint256 _cap
    ) {
        require(_rate > 0, "Rate must be greater than 0");
        require(_cap > 0, "Cap must be greater than 0");
        require(_wallet != address(0), "Invalid wallet address");
        require(address(_token) != address(0), "Invalid token address");

        rate = _rate;
        wallet = _wallet;
        token = _token;
        cap = _cap;
    }

    modifier underCap() {
        require(weiRaised + msg.value <= cap, "Crowdsale cap exceeded");
        _;
    }

    function buyTokens() public payable underCap {
        uint256 weiAmount = msg.value;
        uint256 tokens = weiAmount * rate;

        weiRaised += weiAmount;
        token.transfer(msg.sender, tokens);
        wallet.transfer(weiAmount);
    }

    function capReached() public view returns (bool) {
        return weiRaised >= cap;
    }
}
