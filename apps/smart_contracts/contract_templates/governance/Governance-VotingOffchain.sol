// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SnapshotGovernance {
    address public owner;

    struct Proposal {
        bytes32 snapshotProposalId;
        uint256 voteCount;
        bool executed;
    }

    mapping(bytes32 => Proposal) public proposals;

    constructor() {
        owner = msg.sender;
    }

    function createProposal(bytes32 snapshotProposalId) public {
        require(msg.sender == owner, "Only owner can create proposals");
        proposals[snapshotProposalId] = Proposal({
            snapshotProposalId: snapshotProposalId,
            voteCount: 0,
            executed: false
        });
    }

    function executeProposal(bytes32 snapshotProposalId) public {
        require(msg.sender == owner, "Only owner can execute proposals");
        require(!proposals[snapshotProposalId].executed, "Proposal already executed");

        proposals[snapshotProposalId].executed = true;
    }
}
