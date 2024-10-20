// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TokenMarketplace {
    struct TokenListing {
        address seller;
        address tokenContract;
        uint256 amount;
        uint256 pricePerToken;
    }

    mapping(uint256 => TokenListing) public listings;
    uint256 public listingCount;

    event TokenListed(address indexed seller, uint256 indexed listingId, uint256 amount, uint256 pricePerToken);
    event TokenPurchased(address indexed buyer, uint256 indexed listingId, uint256 amount);

    function listTokens(address tokenContract, uint256 amount, uint256 pricePerToken) public {
        require(amount > 0, "Amount must be greater than 0");
        require(pricePerToken > 0, "Price per token must be greater than 0");

        IERC20(tokenContract).transferFrom(msg.sender, address(this), amount);

        listings[listingCount] = TokenListing({
            seller: msg.sender,
            tokenContract: tokenContract,
            amount: amount,
            pricePerToken: pricePerToken
        });
        listingCount++;

        emit TokenListed(msg.sender, listingCount - 1, amount, pricePerToken);
    }

    function purchaseTokens(uint256 listingId, uint256 amount) public payable {
        TokenListing storage listing = listings[listingId];
        require(amount <= listing.amount, "Not enough tokens available");
        require(msg.value == amount * listing.pricePerToken, "Incorrect payment amount");

        listing.amount -= amount;
        IERC20(listing.tokenContract).transfer(msg.sender, amount);
        payable(listing.seller).transfer(msg.value);

        if (listing.amount == 0) {
            delete listings[listingId];
        }

        emit TokenPurchased(msg.sender, listingId, amount);
    }
}
