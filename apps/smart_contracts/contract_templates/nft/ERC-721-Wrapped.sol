// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract WrappedNFT is ERC20, Ownable {
    ERC721 public nft;
    uint256 public tokenId;

    constructor(address nftAddress, uint256 _tokenId, string memory name, string memory symbol)
        ERC20(name, symbol)
    {
        nft = ERC721(nftAddress);
        tokenId = _tokenId;
    }

    function wrapNFT() public onlyOwner {
        require(nft.ownerOf(tokenId) == msg.sender, "You do not own the NFT");
        nft.transferFrom(msg.sender, address(this), tokenId);
        _mint(msg.sender, 1 * (10 ** decimals()));  // Mint 1 ERC-20 token representing the NFT
    }

    function unwrapNFT() public onlyOwner {
        _burn(msg.sender, 1 * (10 ** decimals()));  // Burn the ERC-20 token
        nft.transferFrom(address(this), msg.sender, tokenId);
    }
}
