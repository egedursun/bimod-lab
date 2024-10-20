// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VerifiedDataOracle {
    address public admin;
    address public trustedSource;
    uint256 public latestData;
    bytes32 public latestDataHash;

    event DataUpdated(uint256 data, bytes32 hash);

    constructor(address _trustedSource) {
        admin = msg.sender;
        trustedSource = _trustedSource;
    }

    function updateTrustedSource(address newSource) public {
        require(msg.sender == admin, "Only admin can update source");
        trustedSource = newSource;
    }

    function updateData(uint256 data, bytes memory signature) public {
        bytes32 dataHash = keccak256(abi.encodePacked(data));
        require(_verifySignature(trustedSource, dataHash, signature), "Invalid signature");

        latestData = data;
        latestDataHash = dataHash;

        emit DataUpdated(data, dataHash);
    }

    function _verifySignature(address signer, bytes32 dataHash, bytes memory signature) internal pure returns (bool) {
        bytes32 ethSignedHash = keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", dataHash));
        (bytes32 r, bytes32 s, uint8 v) = _splitSignature(signature);
        return ecrecover(ethSignedHash, v, r, s) == signer;
    }

    function _splitSignature(bytes memory sig) internal pure returns (bytes32 r, bytes32 s, uint8 v) {
        require(sig.length == 65, "Invalid signature length");
        assembly {
            r := mload(add(sig, 32))
            s := mload(add(sig, 64))
            v := byte(0, mload(add(sig, 96)))
        }
    }
}
