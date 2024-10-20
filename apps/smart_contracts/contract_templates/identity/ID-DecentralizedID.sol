// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DecentralizedIdentity {
    struct Identity {
        address user;
        string didDocument;  // JSON-LD format containing the identity information
        bool verified;
    }

    mapping(address => Identity) public identities;

    event IdentityCreated(address indexed user, string didDocument);
    event IdentityVerified(address indexed user, bool verified);

    function createIdentity(string memory didDocument) public {
        require(bytes(didDocument).length > 0, "Invalid DID document");

        identities[msg.sender] = Identity({
            user: msg.sender,
            didDocument: didDocument,
            verified: false
        });

        emit IdentityCreated(msg.sender, didDocument);
    }

    function verifyIdentity(address user) public {
        require(identities[user].user != address(0), "Identity does not exist");

        identities[user].verified = true;

        emit IdentityVerified(user, true);
    }

    function getIdentity(address user) public view returns (string memory didDocument, bool verified) {
        Identity memory identity = identities[user];
        return (identity.didDocument, identity.verified);
    }
}
