// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CredentialIssuer {
    struct Credential {
        address issuer;
        address holder;
        string credentialData;  // Contains the details of the credential (e.g., qualification)
        bool valid;
    }

    mapping(address => Credential[]) public credentials;

    event CredentialIssued(address indexed issuer, address indexed holder, string credentialData);
    event CredentialRevoked(address indexed issuer, address indexed holder, string credentialData);

    function issueCredential(address holder, string memory credentialData) public {
        require(bytes(credentialData).length > 0, "Invalid credential data");

        credentials[holder].push(Credential({
            issuer: msg.sender,
            holder: holder,
            credentialData: credentialData,
            valid: true
        }));

        emit CredentialIssued(msg.sender, holder, credentialData);
    }

    function revokeCredential(address holder, uint256 credentialIndex) public {
        require(credentials[holder][credentialIndex].issuer == msg.sender, "Only issuer can revoke credential");

        credentials[holder][credentialIndex].valid = false;

        emit CredentialRevoked(msg.sender, holder, credentials[holder][credentialIndex].credentialData);
    }

    function getCredentials(address holder) public view returns (Credential[] memory) {
        return credentials[holder];
    }
}
