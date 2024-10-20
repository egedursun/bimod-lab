// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract RoyaltyMarketplace {
    address public admin;
    uint256 public royaltyPercentage;

    struct Listing {
        address seller;
        address creator;
        address nftContract;
        uint256 tokenId;
        uint256 price;
    }

    mapping(uint256 => Listing) public listings;
    uint256 public listingCount;

    event Listed(address indexed seller, address indexed nftContract, uint256 indexed tokenId, uint256 price);
    event Purchased(address indexed buyer, address indexed nftContract, uint256 indexed tokenId, uint256 price, uint256 royalty);

    constructor(uint256 _royaltyPercentage) {
        admin = msg.sender;
        royaltyPercentage = _royaltyPercentage;
    }

    function listNFT(address nftContract, uint256 tokenId, uint256 price, address creator) public {
        require(price > 0, "Price must be greater than 0");

        IERC721(nftContract).transferFrom(msg.sender, address(this), tokenId);

        listings[listingCount] = Listing({
            seller: msg.sender,
            creator: creator,
            nftContract: nftContract,
            tokenId: tokenId,
            price: price
        });
        listingCount++;

        emit Listed(msg.sender, nftContract, tokenId, price);
    }

    function purchaseNFT(uint256 listingId) public payable {
        Listing memory listing = listings[listingId];
        require(msg.value == listing.price, "Incorrect price");

        uint256 royalty = (listing.price * royaltyPercentage) / 100;
        uint256 sellerAmount = listing.price - royalty;

        IERC721(listing.nftContract).transferFrom(address(this), msg.sender, listing.tokenId);
        payable(listing.seller).transfer(sellerAmount);
        payable(listing.creator).transfer(royalty);

        delete listings[listingId];

        emit Purchased(msg.sender, listing.nftContract, listing.tokenId, listing.price, royalty);
    }
}
