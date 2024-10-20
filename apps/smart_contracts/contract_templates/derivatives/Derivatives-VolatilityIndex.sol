// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract VolatilityIndex is ERC20 {
    uint256 public volatilityIndex;
    uint256 public lastPrice;
    uint256 public priceFluctuation;

    event VolatilityUpdated(uint256 newVolatility);
    event TokensMinted(address indexed minter, uint256 amount);
    event TokensBurned(address indexed burner, uint256 amount);

    constructor(uint256 _initialVolatility) ERC20("VolatilityIndexToken", "VIX") {
        volatilityIndex = _initialVolatility;
    }

    function updateVolatility(uint256 newPrice) public {
        priceFluctuation = (newPrice > lastPrice) ? newPrice - lastPrice : lastPrice - newPrice;
        volatilityIndex = (priceFluctuation * 100) / lastPrice;

        lastPrice = newPrice;

        emit VolatilityUpdated(volatilityIndex);
    }

    function mintTokens(uint256 amount) public {
        _mint(msg.sender, amount);
        emit TokensMinted(msg.sender, amount);
    }

    function burnTokens(uint256 amount) public {
        _burn(msg.sender, amount);
        emit TokensBurned(msg.sender, amount);
    }
}
