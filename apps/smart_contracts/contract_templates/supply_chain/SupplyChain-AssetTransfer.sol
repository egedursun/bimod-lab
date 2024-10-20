// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AssetTransfer {
    struct Asset {
        string description;
        address currentOwner;
        bool isTransferred;
    }

    mapping(uint256 => Asset) public assets;

    event AssetCreated(uint256 indexed assetId, string description, address indexed owner);
    event AssetTransferred(uint256 indexed assetId, address indexed from, address indexed to);

    function createAsset(uint256 assetId, string memory description) public {
        require(assets[assetId].currentOwner == address(0), "Asset already exists");

        assets[assetId] = Asset({
            description: description,
            currentOwner: msg.sender,
            isTransferred: false
        });

        emit AssetCreated(assetId, description, msg.sender);
    }

    function transferAsset(uint256 assetId, address newOwner) public {
        require(assets[assetId].currentOwner == msg.sender, "Only the current owner can transfer the asset");
        require(!assets[assetId].isTransferred, "Asset has already been transferred");

        assets[assetId].currentOwner = newOwner;
        assets[assetId].isTransferred = true;

        emit AssetTransferred(assetId, msg.sender, newOwner);
    }

    function getAssetOwner(uint256 assetId) public view returns (address) {
        return assets[assetId].currentOwner;
    }
}
