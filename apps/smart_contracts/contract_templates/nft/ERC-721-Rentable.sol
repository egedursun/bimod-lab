// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract RentableNFT is ERC721, Ownable {
    struct Rental {
        address renter;
        uint256 expiry;
    }

    mapping(uint256 => Rental) public rentals;

    constructor(string memory name, string memory symbol) ERC721(name, symbol) {}

    function rentNFT(uint256 tokenId, uint256 duration) public payable {
        require(ownerOf(tokenId) == msg.sender, "Only owner can rent");
        require(rentals[tokenId].expiry < block.timestamp, "NFT is already rented");

        rentals[tokenId] = Rental({
            renter: msg.sender,
            expiry: block.timestamp + duration
        });
    }

    function retrieveNFT(uint256 tokenId) public {
        require(block.timestamp > rentals[tokenId].expiry, "Rental period not over");
        _transfer(address(this), ownerOf(tokenId), tokenId);  // Return NFT to owner
    }
}
