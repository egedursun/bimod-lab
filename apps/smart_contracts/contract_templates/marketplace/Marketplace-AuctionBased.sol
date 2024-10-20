// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract AuctionMarketplace {
    struct Auction {
        address seller;
        address nftContract;
        uint256 tokenId;
        uint256 minPrice;
        uint256 highestBid;
        address highestBidder;
        bool ended;
    }

    mapping(uint256 => Auction) public auctions;
    uint256 public auctionCount;

    event AuctionCreated(address indexed seller, uint256 auctionId, uint256 minPrice);
    event BidPlaced(address indexed bidder, uint256 auctionId, uint256 amount);
    event AuctionEnded(address indexed winner, uint256 auctionId, uint256 amount);

    function createAuction(address nftContract, uint256 tokenId, uint256 minPrice) public {
        require(minPrice > 0, "Minimum price must be greater than 0");

        IERC721(nftContract).transferFrom(msg.sender, address(this), tokenId);

        auctions[auctionCount] = Auction({
            seller: msg.sender,
            nftContract: nftContract,
            tokenId: tokenId,
            minPrice: minPrice,
            highestBid: 0,
            highestBidder: address(0),
            ended: false
        });
        auctionCount++;

        emit AuctionCreated(msg.sender, auctionCount - 1, minPrice);
    }

    function placeBid(uint256 auctionId) public payable {
        Auction storage auction = auctions[auctionId];
        require(!auction.ended, "Auction already ended");
        require(msg.value > auction.highestBid, "Bid must be higher than the current highest bid");

        if (auction.highestBidder != address(0)) {
            payable(auction.highestBidder).transfer(auction.highestBid);
        }

        auction.highestBid = msg.value;
        auction.highestBidder = msg.sender;

        emit BidPlaced(msg.sender, auctionId, msg.value);
    }

    function endAuction(uint256 auctionId) public {
        Auction storage auction = auctions[auctionId];
        require(!auction.ended, "Auction already ended");
        require(msg.sender == auction.seller, "Only seller can end the auction");

        auction.ended = true;
        IERC721(auction.nftContract).transferFrom(address(this), auction.highestBidder, auction.tokenId);
        payable(auction.seller).transfer(auction.highestBid);

        emit AuctionEnded(auction.highestBidder, auctionId, auction.highestBid);
    }
}
