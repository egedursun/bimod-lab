// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ERC1155MultiToken is ERC1155, Ownable {
    uint256 public constant GOLD = 0;
    uint256 public constant SILVER = 1;

    constructor(string memory uri) ERC1155(uri) {
        _mint(msg.sender, GOLD, 1000, "");  // Mint 1000 units of fungible GOLD token
        _mint(msg.sender, SILVER, 1, "");   // Mint 1 unit of non-fungible SILVER token
    }
}
