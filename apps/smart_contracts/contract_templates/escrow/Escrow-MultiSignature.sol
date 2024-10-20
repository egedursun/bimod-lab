// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MultiSigEscrow {
    address public depositor;
    address public beneficiary;
    address[3] public approvers;
    mapping(address => bool) public hasApproved;
    uint256 public approvalCount;

    constructor(address _beneficiary, address[3] memory _approvers) payable {
        depositor = msg.sender;
        beneficiary = _beneficiary;
        approvers = _approvers;
    }

    function approve() external {
        require(isApprover(msg.sender), "Not an approver");
        require(!hasApproved[msg.sender], "Already approved");

        hasApproved[msg.sender] = true;
        approvalCount++;

        if (approvalCount >= 2) {
            releaseFunds();
        }
    }

    function isApprover(address _approver) public view returns (bool) {
        for (uint256 i = 0; i < approvers.length; i++) {
            if (approvers[i] == _approver) {
                return true;
            }
        }
        return false;
    }

    function releaseFunds() internal {
        payable(beneficiary).transfer(address(this).balance);
    }

    function cancel() external {
        require(msg.sender == depositor, "Only depositor can cancel");

        payable(depositor).transfer(address(this).balance);
    }
}
