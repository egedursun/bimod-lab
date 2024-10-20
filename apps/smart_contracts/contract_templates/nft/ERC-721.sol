// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract BasicERC721 is ERC721, Ownable {
    uint256 public tokenCounter;

    constructor(string memory name, string memory symbol) ERC721(name, symbol) {
        tokenCounter = 0;
    }

    function createNFT(address recipient) public onlyOwner {
        _safeMint(recipient, tokenCounter);
        tokenCounter++;
    }
}
