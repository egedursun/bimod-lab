// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FuturesContract {
    address public buyer;
    address public seller;
    uint256 public assetPrice;
    uint256 public expirationDate;
    bool public settled;

    event FuturesCreated(address indexed buyer, address indexed seller, uint256 price, uint256 expirationDate);
    event FuturesSettled(address indexed settler, uint256 settlementAmount);

    constructor(address _buyer, address _seller, uint256 _assetPrice, uint256 _expirationDate) {
        buyer = _buyer;
        seller = _seller;
        assetPrice = _assetPrice;
        expirationDate = _expirationDate;
        settled = false;

        emit FuturesCreated(buyer, seller, assetPrice, expirationDate);
    }

    function settle(uint256 currentPrice) public {
        require(block.timestamp >= expirationDate, "Futures contract not yet expired");
        require(!settled, "Futures contract already settled");

        uint256 settlementAmount;

        if (currentPrice > assetPrice) {
            // Buyer profits if the price increases
            settlementAmount = currentPrice - assetPrice;
            payable(buyer).transfer(settlementAmount);
        } else if (currentPrice < assetPrice) {
            // Seller profits if the price decreases
            settlementAmount = assetPrice - currentPrice;
            payable(seller).transfer(settlementAmount);
        }

        settled = true;
        emit FuturesSettled(msg.sender, settlementAmount);
    }
}
