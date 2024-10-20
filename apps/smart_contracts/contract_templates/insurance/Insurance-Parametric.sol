// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IOracle {
    function getEventData() external view returns (bool);
}

contract ParametricInsurance {
    address public insurer;
    address public insured;
    uint256 public premium;
    uint256 public payoutAmount;
    IOracle public oracle;
    bool public policyActive;

    event PolicyActivated(address indexed insured, uint256 premium);
    event PayoutIssued(address indexed insured, uint256 amount);

    constructor(address _insured, uint256 _premium, uint256 _payoutAmount, address _oracle) {
        insurer = msg.sender;
        insured = _insured;
        premium = _premium;
        payoutAmount = _payoutAmount;
        oracle = IOracle(_oracle);
        policyActive = true;
    }

    function activatePolicy() public payable {
        require(msg.sender == insured, "Only the insured can activate the policy");
        require(msg.value == premium, "Incorrect premium amount");
        require(policyActive, "Policy is no longer active");

        emit PolicyActivated(insured, premium);
    }

    function checkEventAndPayout() public {
        require(policyActive, "Policy is no longer active");
        bool eventOccurred = oracle.getEventData();

        if (eventOccurred) {
            payable(insured).transfer(payoutAmount);
            policyActive = false;
            emit PayoutIssued(insured, payoutAmount);
        }
    }

    function getPolicyStatus() public view returns (bool active) {
        return policyActive;
    }
}
