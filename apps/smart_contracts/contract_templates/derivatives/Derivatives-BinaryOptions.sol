// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BinaryOptions {
    enum Outcome {Above, Below}
    address public buyer;
    address public seller;
    uint256 public strikePrice;
    uint256 public expiration;
    Outcome public predictedOutcome;
    bool public settled;

    event OptionPurchased(address indexed buyer, Outcome predictedOutcome, uint256 strikePrice, uint256 expiration);
    event OptionSettled(address indexed settler, bool success);

    constructor(address _buyer, address _seller, uint256 _strikePrice, uint256 _expiration, Outcome _predictedOutcome) {
        buyer = _buyer;
        seller = _seller;
        strikePrice = _strikePrice;
        expiration = _expiration;
        predictedOutcome = _predictedOutcome;
        settled = false;

        emit OptionPurchased(buyer, predictedOutcome, strikePrice, expiration);
    }

    function settle(uint256 currentPrice) public {
        require(block.timestamp >= expiration, "Option has not expired yet");
        require(!settled, "Option has already been settled");

        bool success;

        if ((predictedOutcome == Outcome.Above && currentPrice > strikePrice) ||
            (predictedOutcome == Outcome.Below && currentPrice < strikePrice)) {
            success = true;
            payable(buyer).transfer(address(this).balance);
        } else {
            success = false;
            payable(seller).transfer(address(this).balance);
        }

        settled = true;
        emit OptionSettled(msg.sender, success);
    }
}
