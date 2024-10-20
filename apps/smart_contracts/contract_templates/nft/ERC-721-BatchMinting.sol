// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract BatchMintingERC721 is ERC721Enumerable, Ownable {
    uint256 public tokenCounter;

    constructor(string memory name, string memory symbol) ERC721(name, symbol) {
        tokenCounter = 0;
    }

    function batchMint(address[] memory recipients) public onlyOwner {
        for (uint256 i = 0; i < recipients.length; i++) {
            _safeMint(recipients[i], tokenCounter);
            tokenCounter++;
        }
    }
}
