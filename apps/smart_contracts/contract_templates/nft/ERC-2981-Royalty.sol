// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/interfaces/IERC2981.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ERC721WithRoyalties is ERC721, IERC2981, Ownable {
    address private royaltyRecipient;
    uint256 private royaltyPercentage;

    constructor(string memory name, string memory symbol, address _royaltyRecipient, uint256 _royaltyPercentage)
        ERC721(name, symbol)
    {
        royaltyRecipient = _royaltyRecipient;
        royaltyPercentage = _royaltyPercentage;
    }

    function royaltyInfo(uint256 tokenId, uint256 salePrice) external view override returns (address receiver, uint256 royaltyAmount) {
        royaltyAmount = (salePrice * royaltyPercentage) / 10000;  // Royalties calculated in basis points
        return (royaltyRecipient, royaltyAmount);
    }

    function createNFT(address recipient) public onlyOwner {
        _safeMint(recipient, totalSupply() + 1);
    }
}
