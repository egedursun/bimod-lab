// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MultiSignatureIdentity {
    address[] public verifiers;
    uint256 public requiredSignatures;

    struct Identity {
        address user;
        uint256 signatureCount;
        mapping(address => bool) signatures;
        bool verified;
    }

    mapping(address => Identity) public identities;

    event IdentityVerified(address indexed user);
    event SignatureAdded(address indexed user, address indexed verifier);

    constructor(address[] memory _verifiers, uint256 _requiredSignatures) {
        verifiers = _verifiers;
        requiredSignatures = _requiredSignatures;
    }

    function addSignature(address user) public {
        require(isVerifier(msg.sender), "Only verifiers can add signatures");
        Identity storage identity = identities[user];
        require(!identity.signatures[msg.sender], "Signature already added");

        identity.signatures[msg.sender] = true;
        identity.signatureCount++;

        emit SignatureAdded(user, msg.sender);

        if (identity.signatureCount >= requiredSignatures) {
            identity.verified = true;
            emit IdentityVerified(user);
        }
    }

    function isVerifier(address verifier) public view returns (bool) {
        for (uint256 i = 0; i < verifiers.length; i++) {
            if (verifiers[i] == verifier) {
                return true;
            }
        }
        return false;
    }
}
