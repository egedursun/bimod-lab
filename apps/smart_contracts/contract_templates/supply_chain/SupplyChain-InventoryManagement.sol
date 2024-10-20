// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InventoryManagement {
    struct Product {
        string name;
        uint256 quantity;
    }

    mapping(uint256 => Product) public inventory;

    event ProductAdded(uint256 indexed productId, string name, uint256 quantity);
    event ProductRemoved(uint256 indexed productId, string name, uint256 quantity);

    function addProduct(uint256 productId, string memory name, uint256 quantity) public {
        require(inventory[productId].quantity == 0, "Product already exists in inventory");

        inventory[productId] = Product({
            name: name,
            quantity: quantity
        });

        emit ProductAdded(productId, name, quantity);
    }

    function removeProduct(uint256 productId, uint256 quantity) public {
        require(inventory[productId].quantity >= quantity, "Insufficient stock");

        inventory[productId].quantity -= quantity;

        emit ProductRemoved(productId, inventory[productId].name, quantity);
    }

    function getProductQuantity(uint256 productId) public view returns (uint256) {
        return inventory[productId].quantity;
    }
}
