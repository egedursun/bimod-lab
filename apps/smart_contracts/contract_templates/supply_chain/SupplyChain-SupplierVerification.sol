// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SupplierVerification {
    struct Supplier {
        string name;
        bool isVerified;
    }

    mapping(address => Supplier) public suppliers;
    address public verifier;

    event SupplierVerified(address indexed supplier, string name);
    event SupplierRejected(address indexed supplier, string name);

    constructor() {
        verifier = msg.sender;
    }

    function verifySupplier(address supplierAddress, string memory name) public {
        require(msg.sender == verifier, "Only the verifier can approve suppliers");

        suppliers[supplierAddress] = Supplier({
            name: name,
            isVerified: true
        });

        emit SupplierVerified(supplierAddress, name);
    }

    function rejectSupplier(address supplierAddress, string memory name) public {
        require(msg.sender == verifier, "Only the verifier can reject suppliers");

        suppliers[supplierAddress].isVerified = false;

        emit SupplierRejected(supplierAddress, name);
    }

    function isSupplierVerified(address supplierAddress) public view returns (bool) {
        return suppliers[supplierAddress].isVerified;
    }
}
