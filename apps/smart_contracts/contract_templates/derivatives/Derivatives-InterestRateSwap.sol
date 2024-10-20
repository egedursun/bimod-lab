// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InterestRateSwap {
    address public fixedPayer;
    address public floatingPayer;
    uint256 public notionalAmount;
    uint256 public fixedRate;
    uint256 public floatingRate;
    uint256 public settlementPeriod;
    uint256 public lastSettlementTime;

    event SwapCreated(address indexed fixedPayer, address indexed floatingPayer, uint256 notionalAmount, uint256 fixedRate, uint256 floatingRate);
    event SwapSettled(address indexed settler, uint256 fixedPayment, uint256 floatingPayment);

    constructor(
        address _fixedPayer,
        address _floatingPayer,
        uint256 _notionalAmount,
        uint256 _fixedRate,
        uint256 _floatingRate,
        uint256 _settlementPeriod
    ) {
        fixedPayer = _fixedPayer;
        floatingPayer = _floatingPayer;
        notionalAmount = _notionalAmount;
        fixedRate = _fixedRate;
        floatingRate = _floatingRate;
        settlementPeriod = _settlementPeriod;
        lastSettlementTime = block.timestamp;

        emit SwapCreated(fixedPayer, floatingPayer, notionalAmount, fixedRate, floatingRate);
    }

    function settleSwap() public {
        require(block.timestamp >= lastSettlementTime + settlementPeriod, "Settlement period not reached");

        uint256 fixedPayment = (notionalAmount * fixedRate) / 100;
        uint256 floatingPayment = (notionalAmount * floatingRate) / 100;

        if (fixedPayment > floatingPayment) {
            payable(fixedPayer).transfer(fixedPayment - floatingPayment);
        } else {
            payable(floatingPayer).transfer(floatingPayment - fixedPayment);
        }

        lastSettlementTime = block.timestamp;

        emit SwapSettled(msg.sender, fixedPayment, floatingPayment);
    }
}
