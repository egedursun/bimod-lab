// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FractionalOwnership {
    struct FractionalOwner {
        address owner;
        uint256 ownershipPercentage;
    }

    FractionalOwner[] public owners;
    uint256 public totalOwnership;

    event OwnershipTransferred(address indexed from, address indexed to, uint256 ownershipPercentage);

    function addOwner(address newOwner, uint256 ownershipPercentage) public {
        require(ownershipPercentage + totalOwnership <= 100, "Total ownership cannot exceed 100%");
        owners.push(FractionalOwner(newOwner, ownershipPercentage));
        totalOwnership += ownershipPercentage;
    }

    function transferOwnership(address from, address to, uint256 percentage) public {
        for (uint256 i = 0; i < owners.length; i++) {
            if (owners[i].owner == from && owners[i].ownershipPercentage >= percentage) {
                owners[i].ownershipPercentage -= percentage;
                owners.push(FractionalOwner(to, percentage));

                emit OwnershipTransferred(from, to, percentage);
                return;
            }
        }

        revert("Ownership transfer failed");
    }

    function getOwners() public view returns (FractionalOwner[] memory) {
        return owners;
    }
}
