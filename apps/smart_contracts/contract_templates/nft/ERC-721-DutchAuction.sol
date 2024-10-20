// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract DutchAuction is Ownable {
    ERC721 public nft;
    uint256 public auctionEndTime;
    uint256 public startingPrice;
    uint256 public endingPrice;
    uint256 public priceDecrement;
    address public highestBidder;

    constructor(
        address nftAddress,
        uint256 duration,
        uint256 _startingPrice,
        uint256 _endingPrice
    ) {
        nft = ERC721(nftAddress);
        auctionEndTime = block.timestamp + duration;
        startingPrice = _startingPrice;
        endingPrice = _endingPrice;
        priceDecrement = (startingPrice - endingPrice) / duration;
    }

    function getCurrentPrice() public view returns (uint256) {
        uint256 elapsedTime = block.timestamp > auctionEndTime ? auctionEndTime - block.timestamp : 0;
        return startingPrice - (elapsedTime * priceDecrement);
    }

    function buyNFT(uint256 tokenId) public payable {
        require(block.timestamp < auctionEndTime, "Auction has ended");
        uint256 currentPrice = getCurrentPrice();
        require(msg.value >= currentPrice, "Insufficient payment");

        highestBidder = msg.sender;
        nft.transferFrom(owner(), highestBidder, tokenId);
    }
}
