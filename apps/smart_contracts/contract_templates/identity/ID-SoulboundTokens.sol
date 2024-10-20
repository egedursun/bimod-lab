// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SoulboundToken is ERC721 {
    address public issuer;

    event SBTMinted(address indexed owner, uint256 tokenId);

    constructor() ERC721("SoulboundToken", "SBT") {
        issuer = msg.sender;
    }

    function mintSBT(address recipient, uint256 tokenId) public {
        require(msg.sender == issuer, "Only issuer can mint SBTs");
        _mint(recipient, tokenId);

        emit SBTMinted(recipient, tokenId);
    }

    function _transfer(address from, address to, uint256 tokenId) internal pure override {
        revert("SBTs are non-transferable");
    }
}
