// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CreditDefaultSwap {
    address public protectionBuyer;
    address public protectionSeller;
    uint256 public notionalAmount;
    uint256 public premium;
    uint256 public settlementPeriod;
    uint256 public lastPaymentTime;
    bool public defaultOccurred;

    event SwapCreated(address indexed buyer, address indexed seller, uint256 notionalAmount, uint256 premium);
    event DefaultOccurred();
    event ProtectionPaid(address indexed seller, uint256 payout);

    constructor(
        address _protectionBuyer,
        address _protectionSeller,
        uint256 _notionalAmount,
        uint256 _premium,
        uint256 _settlementPeriod
    ) {
        protectionBuyer = _protectionBuyer;
        protectionSeller = _protectionSeller;
        notionalAmount = _notionalAmount;
        premium = _premium;
        settlementPeriod = _settlementPeriod;
        lastPaymentTime = block.timestamp;

        emit SwapCreated(protectionBuyer, protectionSeller, notionalAmount, premium);
    }

    function payPremium() public {
        require(block.timestamp >= lastPaymentTime + settlementPeriod, "Premium not yet due");

        payable(protectionSeller).transfer(premium);
        lastPaymentTime = block.timestamp;
    }

    function reportDefault() public {
        require(msg.sender == protectionBuyer, "Only buyer can report default");
        defaultOccurred = true;

        emit DefaultOccurred();
    }

    function payoutProtection() public {
        require(defaultOccurred, "No default reported");

        payable(protectionBuyer).transfer(notionalAmount);
        emit ProtectionPaid(protectionSeller, notionalAmount);
    }
}
