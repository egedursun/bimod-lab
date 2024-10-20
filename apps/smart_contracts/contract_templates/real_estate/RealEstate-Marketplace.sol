// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RealEstateMarketplace {
    struct Property {
        address owner;
        string details;
        uint256 price;
        bool forSale;
    }

    mapping(uint256 => Property) public properties;
    uint256 public propertyCount;

    event PropertyListed(uint256 indexed propertyId, string details, uint256 price);
    event PropertySold(uint256 indexed propertyId, address newOwner, uint256 price);

    function listProperty(string memory details, uint256 price) public {
        propertyCount++;
        properties[propertyCount] = Property({
            owner: msg.sender,
            details: details,
            price: price,
            forSale: true
        });

        emit PropertyListed(propertyCount, details, price);
    }

    function buyProperty(uint256 propertyId) public payable {
        Property storage property = properties[propertyId];
        require(property.forSale, "Property is not for sale");
        require(msg.value == property.price, "Incorrect price");

        property.owner = msg.sender;
        property.forSale = false;

        payable(property.owner).transfer(msg.value);

        emit PropertySold(propertyId, msg.sender, msg.value);
    }

    function getPropertyDetails(uint256 propertyId) public view returns (address owner, string memory details, uint256 price, bool forSale) {
        Property memory property = properties[propertyId];
        return (property.owner, property.details, property.price, property.forSale);
    }
}
