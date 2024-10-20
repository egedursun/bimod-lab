// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC1155/IERC1155.sol";

contract SimpleNFTMarketplace {
    address public admin;
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

    function listNFT(address nftContract, uint256 tokenId, uint256 price) public {
        require(price > 0, "Price must be greater than 0");

        if (IERC721(nftContract).supportsInterface(0x80ac58cd)) {
            IERC721(nftContract).transferFrom(msg.sender, address(this), tokenId);
        } else if (IERC1155(nftContract).supportsInterface(0xd9b67a26)) {
            IERC1155(nftContract).safeTransferFrom(msg.sender, address(this), tokenId, 1, "");
        } else {
            revert("Unsupported NFT standard");
        }

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
        Listing memory listing = listings[listingId];
        require(msg.value == listing.price, "Incorrect price");

        if (IERC721(listing.nftContract).supportsInterface(0x80ac58cd)) {
            IERC721(listing.nftContract).transferFrom(address(this), msg.sender, listing.tokenId);
        } else if (IERC1155(listing.nftContract).supportsInterface(0xd9b67a26)) {
            IERC1155(listing.nftContract).safeTransferFrom(address(this), msg.sender, listing.tokenId, 1, "");
        }

        payable(listing.seller).transfer(listing.price);
        delete listings[listingId];

        emit Purchased(msg.sender, listing.nftContract, listing.tokenId, listing.price);
    }
}
