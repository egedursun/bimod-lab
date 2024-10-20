// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract NFTStaking is Ownable {
    ERC721 public nft;
    mapping(uint256 => address) public tokenOwners;
    mapping(uint256 => uint256) public stakingStartTime;

    constructor(address nftAddress) {
        nft = ERC721(nftAddress);
    }

    function stakeNFT(uint256 tokenId) public {
        require(nft.ownerOf(tokenId) == msg.sender, "You are not the owner");
        nft.transferFrom(msg.sender, address(this), tokenId);
        tokenOwners[tokenId] = msg.sender;
        stakingStartTime[tokenId] = block.timestamp;
    }

    function unstakeNFT(uint256 tokenId) public {
        require(tokenOwners[tokenId] == msg.sender, "You are not the staker");
        nft.transferFrom(address(this), msg.sender, tokenId);
        delete tokenOwners[tokenId];
        delete stakingStartTime[tokenId];
    }

    function calculateRewards(uint256 tokenId) public view returns (uint256) {
        uint256 stakedTime = block.timestamp - stakingStartTime[tokenId];
        return stakedTime / 1 days;  // Example: 1 reward per day
    }
}
