// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TieredPricingCrowdsale {
    IERC20 public token;
    address payable public wallet;
    uint256 public weiRaised;

    struct Tier {
        uint256 rate;
        uint256 weiLimit;
    }

    Tier[] public tiers;
    uint256 public currentTierIndex;

    constructor(address payable _wallet, IERC20 _token) {
        wallet = _wallet;
        token = _token;

        // Define tiered pricing structure (lower rates mean cheaper tokens)
        tiers.push(Tier({rate: 500, weiLimit: 100 ether}));
        tiers.push(Tier({rate: 400, weiLimit: 200 ether}));
        tiers.push(Tier({rate: 300, weiLimit: 500 ether}));
        currentTierIndex = 0;
    }

    function buyTokens() public payable {
        require(currentTierIndex < tiers.length, "No more tiers available");

        Tier storage tier = tiers[currentTierIndex];
        uint256 weiAmount = msg.value;
        uint256 tokens = weiAmount * tier.rate;

        weiRaised += weiAmount;
        token.transfer(msg.sender, tokens);
        wallet.transfer(weiAmount);

        if (weiRaised >= tier.weiLimit) {
            currentTierIndex++;
        }
    }

    function getCurrentTier() public view returns (uint256) {
        return currentTierIndex;
    }
}
