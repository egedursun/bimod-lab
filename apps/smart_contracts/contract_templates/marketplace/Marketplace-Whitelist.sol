// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract WhitelistMarketplace {
    address public admin;
    mapping(address => bool) public whitelist;

    struct Listing {
        address seller;
        address nftContract;
        uint256 tokenId;
        uint256 price;
    }

    mapping(uint256 => Listing) public listings;
    uint256 public listingCount;

    event Listed(address indexed seller, address indexed nftContract, uint256 indexed tokenId, uint256 price);
    event Purchased(address indexed buyer, address indexed nftContract, uint256 indexed tokenId, uint256 price);

    constructor() {
        admin = msg.sender;
    }

    function addToWhitelist(address user) public {
        require(msg.sender == admin, "Only admin can add to whitelist");
        whitelist[user] = true;
    }

    function removeFromWhitelist(address user) public {
        require(msg.sender == admin, "Only admin can remove from whitelist");
        whitelist[user] = false;
    }

    function listNFT(address nftContract, uint256 tokenId, uint256 price) public {
        require(whitelist[msg.sender], "Not on whitelist");

        IERC721(nftContract).transferFrom(msg.sender, address(this), tokenId);

        listings[listingCount] = Listing({
            seller: msg.sender,
            nftContract: nftContract,
            tokenId: tokenId,
            price: price
        });
        listingCount++;

        emit Listed(msg.sender, nftContract, tokenId, price);
    }

    function purchaseNFT(uint256 listingId) public payable {
        require(whitelist[msg.sender], "Not on whitelist");

        Listing memory listing = listings[listingId];
        require(msg.value == listing.price, "Incorrect price");

        IERC721(listing.nftContract).transferFrom(address(this), msg.sender, listing.tokenId);
        payable(listing.seller).transfer(listing.price);

        delete listings[listingId];

        emit Purchased(msg.sender, listing.nftContract, listing.tokenId, listing.price);
    }
}
