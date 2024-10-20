// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract FractionalNFT is ERC20, Ownable {
    ERC721 public nft;
    uint256 public tokenId;

    constructor(address nftAddress, uint256 _tokenId, string memory name, string memory symbol, uint256 supply)
        ERC20(name, symbol)
    {
        nft = ERC721(nftAddress);
        tokenId = _tokenId;
        _mint(msg.sender, supply);
    }

    function fractionalizeNFT() public onlyOwner {
        require(nft.ownerOf(tokenId) == msg.sender, "You do not own the NFT");
        nft.transferFrom(msg.sender, address(this), tokenId);
    }

    function redeemNFT() public onlyOwner {
        nft.transferFrom(address(this), msg.sender, tokenId);
    }
}
