// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertificationVerification {
    struct Certification {
        string certName;
        uint256 issuedDate;
        uint256 expiryDate;
        bool isValid;
    }

    mapping(address => Certification) public certifications;

    event CertificationIssued(address indexed entity, string certName, uint256 issuedDate, uint256 expiryDate);
    event CertificationRevoked(address indexed entity, string certName);

    function issueCertification(address entity, string memory certName, uint256 expiryDate) public {
        certifications[entity] = Certification({
            certName: certName,
            issuedDate: block.timestamp,
            expiryDate: expiryDate,
            isValid: true
        });

        emit CertificationIssued(entity, certName, block.timestamp, expiryDate);
    }

    function revokeCertification(address entity) public {
        certifications[entity].isValid = false;

        emit CertificationRevoked(entity, certifications[entity].certName);
    }

    function isCertified(address entity) public view returns (bool) {
        return certifications[entity].isValid && block.timestamp <= certifications[entity].expiryDate;
    }
}
