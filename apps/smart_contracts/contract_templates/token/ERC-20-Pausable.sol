// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract PausableERC20 is ERC20Pausable, Ownable {
    constructor(string memory name, string memory symbol, uint256 initialSupply) ERC20(name, symbol) {
        _mint(msg.sender, initialSupply * (10 ** decimals()));
    }

    // Function to pause transfers
    function pause() public onlyOwner {
        _pause();
    }

    // Function to unpause transfers
    function unpause() public onlyOwner {
        _unpause();
    }
}
