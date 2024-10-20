// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RevenueSharingMarketplace {
    struct RevenueShare {
        address recipient;
        uint256 percentage;
    }

    struct Listing {
        address seller;
        address nftContract;
        uint256 tokenId;
        uint256 price;
        RevenueShare[] shares;
    }

    mapping(uint256 => Listing) public listings;
    uint256 public listingCount;

    event Listed(address indexed seller, address indexed nftContract, uint256 indexed tokenId, uint256 price);
    event Purchased(address indexed buyer, address indexed nftContract, uint256 indexed tokenId, uint256 price);

    function listNFTWithRevenueShares(
        address nftContract,
        uint256 tokenId,
        uint256 price,
        RevenueShare[] memory revenueShares
    ) public {
        require(price > 0, "Price must be greater than 0");

        Listing storage listing = listings[listingCount];
        listing.seller = msg.sender;
        listing.nftContract = nftContract;
        listing.tokenId = tokenId;
        listing.price = price;

        for (uint256 i = 0; i < revenueShares.length; i++) {
            listing.shares.push(revenueShares[i]);
        }

        listingCount++;

        emit Listed(msg.sender, nftContract, tokenId, price);
    }

    function purchaseNFT(uint256 listingId) public payable {
        Listing storage listing = listings[listingId];
        require(msg.value == listing.price, "Incorrect price");

        uint256 totalRevenue = msg.value;
        for (uint256 i = 0; i < listing.shares.length; i++) {
            uint256 shareAmount = (totalRevenue * listing.shares[i].percentage) / 100;
            payable(listing.shares[i].recipient).transfer(shareAmount);
        }

        uint256 sellerRevenue = totalRevenue;
        for (uint256 i = 0; i < listing.shares.length; i++) {
            uint256 shareAmount = (totalRevenue * listing.shares[i].percentage) / 100;
            sellerRevenue -= shareAmount;
        }

        payable(listing.seller).transfer(sellerRevenue);
        IERC721(listing.nftContract).transferFrom(listing.seller, msg.sender, listing.tokenId);

        emit Purchased(msg.sender, listing.nftContract, listing.tokenId, listing.price);
    }
}
