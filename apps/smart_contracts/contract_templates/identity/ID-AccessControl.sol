// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IdentityAccessControl {
    mapping(address => bool) public verifiedUsers;
    address public admin;

    event UserVerified(address indexed user);
    event UserAccessGranted(address indexed user);

    constructor() {
        admin = msg.sender;
    }

    function verifyUser(address user) public {
        require(msg.sender == admin, "Only admin can verify users");

        verifiedUsers[user] = true;

        emit UserVerified(user);
    }

    modifier onlyVerified() {
        require(verifiedUsers[msg.sender], "Access restricted to verified users");
        _;
    }

    function accessProtectedResource() public onlyVerified {
        // Protected resource that only verified users can access
        emit UserAccessGranted(msg.sender);
    }
}
