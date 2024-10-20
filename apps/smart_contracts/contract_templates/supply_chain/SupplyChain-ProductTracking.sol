// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ProductTracking {
    struct Product {
        string name;
        string serialNumber;
        address currentOwner;
        string[] history;
    }

    mapping(string => Product) public products;

    event ProductCreated(string serialNumber, string name, address indexed owner);
    event ProductTransferred(string serialNumber, address indexed from, address indexed to);

    function createProduct(string memory name, string memory serialNumber) public {
        require(products[serialNumber].currentOwner == address(0), "Product already exists");

        products[serialNumber] = Product({
            name: name,
            serialNumber: serialNumber,
            currentOwner: msg.sender,
            history: new string
        });

        products[serialNumber].history.push("Created");

        emit ProductCreated(serialNumber, name, msg.sender);
    }

    function transferProduct(string memory serialNumber, address newOwner) public {
        require(products[serialNumber].currentOwner == msg.sender, "Only the current owner can transfer the product");

        products[serialNumber].history.push("Transferred to new owner");
        products[serialNumber].currentOwner = newOwner;

        emit ProductTransferred(serialNumber, msg.sender, newOwner);
    }

    function getProductHistory(string memory serialNumber) public view returns (string[] memory) {
        return products[serialNumber].history;
    }
}
