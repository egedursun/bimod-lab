// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract OptionsContract {
    enum OptionType { Call, Put }

    address public buyer;
    address public seller;
    OptionType public optionType;
    uint256 public strikePrice;
    uint256 public expirationDate;
    bool public exercised;

    event OptionCreated(address indexed buyer, address indexed seller, OptionType optionType, uint256 strikePrice, uint256 expirationDate);
    event OptionExercised(address indexed exerciser, uint256 amount);

    constructor(address _buyer, address _seller, OptionType _optionType, uint256 _strikePrice, uint256 _expirationDate) {
        buyer = _buyer;
        seller = _seller;
        optionType = _optionType;
        strikePrice = _strikePrice;
        expirationDate = _expirationDate;
        exercised = false;

        emit OptionCreated(buyer, seller, optionType, strikePrice, expirationDate);
    }

    function exercise(uint256 currentPrice) public {
        require(block.timestamp <= expirationDate, "Option expired");
        require(!exercised, "Option already exercised");

        uint256 payout;

        if (optionType == OptionType.Call && currentPrice > strikePrice) {
            // Call option: buyer profits if the price exceeds the strike price
            payout = currentPrice - strikePrice;
            payable(buyer).transfer(payout);
        } else if (optionType == OptionType.Put && currentPrice < strikePrice) {
            // Put option: buyer profits if the price falls below the strike price
            payout = strikePrice - currentPrice;
            payable(buyer).transfer(payout);
        }

        exercised = true;
        emit OptionExercised(msg.sender, payout);
    }
}
