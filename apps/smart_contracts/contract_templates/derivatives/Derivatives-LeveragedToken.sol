// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract LeveragedToken is ERC20 {
    address public admin;
    uint256 public leverageRatio;
    uint256 public lastPrice;

    event TokenMinted(address indexed minter, uint256 amount, uint256 price);
    event TokenBurned(address indexed burner, uint256 amount);

    constructor(uint256 _initialSupply, uint256 _leverageRatio) ERC20("LeveragedToken", "LEV") {
        _mint(msg.sender, _initialSupply);
        leverageRatio = _leverageRatio;
        admin = msg.sender;
    }

    function updatePrice(uint256 newPrice) public {
        require(msg.sender == admin, "Only admin can update price");

        uint256 priceChange = (newPrice * leverageRatio) / lastPrice;
        _adjustTokenSupply(priceChange);

        lastPrice = newPrice;
    }

    function _adjustTokenSupply(uint256 priceChange) internal {
        uint256 totalSupplyChange = (totalSupply() * priceChange) / 100;
        _mint(admin, totalSupplyChange);
    }

    function mintTokens(uint256 amount) public {
        _mint(msg.sender, amount);
        emit TokenMinted(msg.sender, amount, lastPrice);
    }

    function burnTokens(uint256 amount) public {
        _burn(msg.sender, amount);
        emit TokenBurned(msg.sender, amount);
    }
}
