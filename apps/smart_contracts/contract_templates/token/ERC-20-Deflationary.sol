// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract DeflationaryERC20 is ERC20 {
    uint256 public burnPercentage;

    constructor(string memory name, string memory symbol, uint256 initialSupply, uint256 _burnPercentage)
        ERC20(name, symbol)
    {
        _mint(msg.sender, initialSupply * (10 ** decimals()));
        burnPercentage = _burnPercentage;
    }

    function _transfer(address sender, address recipient, uint256 amount) internal override {
        uint256 burnAmount = (amount * burnPercentage) / 100;
        uint256 amountAfterBurn = amount - burnAmount;

        super._burn(sender, burnAmount);  // Burn the tokens
        super._transfer(sender, recipient, amountAfterBurn);  // Transfer remaining tokens
    }
}
