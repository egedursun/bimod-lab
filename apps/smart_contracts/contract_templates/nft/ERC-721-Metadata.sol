// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ERC721WithMetadata is ERC721URIStorage, Ownable {
    uint256 public tokenCounter;

    constructor(string memory name, string memory symbol) ERC721(name, symbol) {
        tokenCounter = 0;
    }

    function createNFT(address recipient, string memory tokenURI) public onlyOwner {
        _safeMint(recipient, tokenCounter);
        _setTokenURI(tokenCounter, tokenURI);  // Set metadata URI for the token
        tokenCounter++;
    }
}
