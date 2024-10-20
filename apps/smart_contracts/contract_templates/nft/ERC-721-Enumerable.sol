// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ERC721EnumerableNFT is ERC721Enumerable, Ownable {
    uint256 public tokenCounter;

    constructor(string memory name, string memory symbol) ERC721(name, symbol) {
        tokenCounter = 0;
    }

    function createNFT(address recipient) public onlyOwner {
        _safeMint(recipient, tokenCounter);
        tokenCounter++;
    }
}
