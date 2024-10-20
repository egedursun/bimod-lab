// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RealTimeRoyaltySplitter {
    address[] public recipients;
    uint256[] public percentages;
    uint256 public totalPercentage;

    event RoyaltiesSplit(uint256 totalAmount, uint256 splitAmount, address recipient);

    constructor(address[] memory _recipients, uint256[] memory _percentages) {
        require(_recipients.length == _percentages.length, "Recipients and percentages length mismatch");

        recipients = _recipients;
        percentages = _percentages;

        for (uint256 i = 0; i < _percentages.length; i++) {
            totalPercentage += _percentages[i];
        }

        require(totalPercentage == 100, "Total percentages must equal 100");
    }

    function splitRoyalties() public payable {
        require(msg.value > 0, "No royalties to split");

        for (uint256 i = 0; i < recipients.length; i++) {
            uint256 amount = (msg.value * percentages[i]) / 100;
            payable(recipients[i]).transfer(amount);
            emit RoyaltiesSplit(msg.value, amount, recipients[i]);
        }
    }
}
