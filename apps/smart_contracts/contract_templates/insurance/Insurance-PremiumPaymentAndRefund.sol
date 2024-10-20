// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InsurancePremiumRefund {
    address public policyholder;
    uint256 public premium;
    uint256 public policyDuration;
    uint256 public policyStart;
    bool public policyActive;

    event PolicyCreated(address indexed policyholder, uint256 premium, uint256 policyDuration);
    event PremiumRefunded(address indexed policyholder, uint256 refundAmount);

    constructor(address _policyholder, uint256 _premium, uint256 _policyDuration) {
        policyholder = _policyholder;
        premium = _premium;
        policyDuration = _policyDuration;
        policyStart = block.timestamp;
        policyActive = true;

        emit PolicyCreated(policyholder, premium, policyDuration);
    }

    function cancelPolicy() public {
        require(msg.sender == policyholder, "Only the policyholder can cancel the policy");
        require(policyActive, "Policy is not active");

        uint256 timeElapsed = block.timestamp - policyStart;
        uint256 refundAmount = (premium * (policyDuration - timeElapsed)) / policyDuration;

        policyActive = false;
        payable(policyholder).transfer(refundAmount);

        emit PremiumRefunded(policyholder, refundAmount);
    }

    function getPolicyStatus() public view returns (bool) {
        return policyActive;
    }
}
