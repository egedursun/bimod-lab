// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ServiceMarketplace {
    struct ServiceListing {
        address provider;
        string description;
        uint256 price;
        bool isAvailable;
    }

    mapping(uint256 => ServiceListing) public listings;
    uint256 public listingCount;

    event ServiceListed(address indexed provider, uint256 indexed listingId, uint256 price, string description);
    event ServicePurchased(address indexed buyer, uint256 indexed listingId, uint256 price);

    function listService(string memory description, uint256 price) public {
        require(price > 0, "Price must be greater than 0");

        listings[listingCount] = ServiceListing({
            provider: msg.sender,
            description: description,
            price: price,
            isAvailable: true
        });
        listingCount++;

        emit ServiceListed(msg.sender, listingCount - 1, price, description);
    }

    function purchaseService(uint256 listingId) public payable {
        ServiceListing storage listing = listings[listingId];
        require(listing.isAvailable, "Service no longer available");
        require(msg.value == listing.price, "Incorrect payment amount");

        listing.isAvailable = false;
        payable(listing.provider).transfer(msg.value);

        emit ServicePurchased(msg.sender, listingId, listing.price);
    }
}
