// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract WhitelistedCrowdsale is Ownable {
    IERC20 public token;
    address payable public wallet;
    uint256 public rate;
    uint256 public weiRaised;
    mapping(address => bool) public whitelist;

    constructor(uint256 _rate, address payable _wallet, IERC20 _token) {
        require(_rate > 0, "Rate must be greater than 0");
        require(_wallet != address(0), "Invalid wallet address");
        require(address(_token) != address(0), "Invalid token address");

        rate = _rate;
        wallet = _wallet;
        token = _token;
    }

    modifier onlyWhitelisted() {
        require(whitelist[msg.sender], "Not whitelisted");
        _;
    }

    function addToWhitelist(address participant) public onlyOwner {
        whitelist[participant] = true;
    }

    function removeFromWhitelist(address participant) public onlyOwner {
        whitelist[participant] = false;
    }

    function buyTokens() public payable onlyWhitelisted {
        uint256 weiAmount = msg.value;
        require(weiAmount > 0, "Ether amount is 0");

        uint256 tokens = weiAmount * rate;
        weiRaised += weiAmount;

        token.transfer(msg.sender, tokens);
        wallet.transfer(msg.value);
    }
}
