// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract TaxableERC20 is ERC20, Ownable {
    uint256 public taxPercentage;  // Tax as a percentage of the transfer
    address public taxRecipient;  // Address where tax is sent

    constructor(
        string memory name,
        string memory symbol,
        uint256 initialSupply,
        uint256 _taxPercentage,
        address _taxRecipient
    ) ERC20(name, symbol) {
        require(_taxRecipient != address(0), "Invalid tax recipient");

        _mint(msg.sender, initialSupply * (10 ** decimals()));
        taxPercentage = _taxPercentage;
        taxRecipient = _taxRecipient;
    }

    function _transfer(address sender, address recipient, uint256 amount) internal override {
        uint256 taxAmount = (amount * taxPercentage) / 100;
        uint256 amountAfterTax = amount - taxAmount;

        super._transfer(sender, taxRecipient, taxAmount);  // Transfer tax to taxRecipient
        super._transfer(sender, recipient, amountAfterTax);  // Transfer remaining tokens
    }
}
