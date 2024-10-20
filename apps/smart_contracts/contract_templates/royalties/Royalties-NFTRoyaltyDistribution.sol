// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract NFTRoyalties is ERC721, Ownable {
    uint256 public royaltyPercentage;

    event RoyaltiesPaid(address indexed recipient, uint256 amount);

    constructor(string memory name, string memory symbol, uint256 _royaltyPercentage) ERC721(name, symbol) {
        royaltyPercentage = _royaltyPercentage;
    }

    function _transfer(address from, address to, uint256 tokenId) internal override {
        super._transfer(from, to, tokenId);

        uint256 salePrice = msg.value;
        uint256 royaltyAmount = (salePrice * royaltyPercentage) / 100;
        payable(owner()).transfer(royaltyAmount);

        emit RoyaltiesPaid(owner(), royaltyAmount);
    }
}
