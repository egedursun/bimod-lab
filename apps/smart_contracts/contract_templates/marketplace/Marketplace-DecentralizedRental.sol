// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract NFTRentalMarketplace {
    address public admin;

    struct Rental {
        address owner;
        address renter;
        address nftContract;
        uint256 tokenId;
        uint256 rentalPrice;
        uint256 rentalPeriod;
        uint256 rentalStartTime;
        bool isRented;
    }

    mapping(uint256 => Rental) public rentals;
    uint256 public rentalCount;

    event NFTListedForRent(address indexed owner, address indexed nftContract, uint256 indexed tokenId, uint256 price, uint256 period);
    event NFTRented(address indexed renter, address indexed nftContract, uint256 indexed tokenId, uint256 price, uint256 period);

    constructor() {
        admin = msg.sender;
    }

    function listNFTForRent(address nftContract, uint256 tokenId, uint256 price, uint256 period) public {
        require(price > 0, "Rental price must be greater than 0");
        require(period > 0, "Rental period must be greater than 0");

        IERC721(nftContract).transferFrom(msg.sender, address(this), tokenId);

        rentals[rentalCount] = Rental({
            owner: msg.sender,
            renter: address(0),
            nftContract: nftContract,
            tokenId: tokenId,
            rentalPrice: price,
            rentalPeriod: period,
            rentalStartTime: 0,
            isRented: false
        });
        rentalCount++;

        emit NFTListedForRent(msg.sender, nftContract, tokenId, price, period);
    }

    function rentNFT(uint256 rentalId) public payable {
        Rental storage rental = rentals[rentalId];
        require(msg.value == rental.rentalPrice, "Incorrect rental price");
        require(!rental.isRented, "NFT is already rented");

        rental.renter = msg.sender;
        rental.rentalStartTime = block.timestamp;
        rental.isRented = true;

        payable(rental.owner).transfer(rental.rentalPrice);

        emit NFTRented(msg.sender, rental.nftContract, rental.tokenId, rental.rentalPrice, rental.rentalPeriod);
    }

    function returnNFT(uint256 rentalId) public {
        Rental storage rental = rentals[rentalId];
        require(rental.renter == msg.sender, "Only the renter can return the NFT");
        require(block.timestamp >= rental.rentalStartTime + rental.rentalPeriod, "Rental period not yet over");

        IERC721(rental.nftContract).transferFrom(address(this), rental.owner, rental.tokenId);
        rental.isRented = false;
        rental.renter = address(0);
        rental.rentalStartTime = 0;
    }
}
