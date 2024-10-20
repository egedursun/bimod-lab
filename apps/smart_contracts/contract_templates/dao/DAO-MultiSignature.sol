// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MultiSigDAO {
    address[] public signatories;
    uint256 public requiredSignatures;

    struct Proposal {
        address payable recipient;
        uint256 amount;
        uint256 signatures;
        bool executed;
    }

    Proposal[] public proposals;
    mapping(uint256 => mapping(address => bool)) public hasSigned;

    constructor(address[] memory _signatories, uint256 _requiredSignatures) {
        signatories = _signatories;
        requiredSignatures = _requiredSignatures;
    }

    function createProposal(address payable recipient, uint256 amount) public {
        require(isSignatory(msg.sender), "Not a signatory");

        proposals.push(Proposal({
            recipient: recipient,
            amount: amount,
            signatures: 0,
            executed: false
        }));
    }

    function signProposal(uint256 proposalId) public {
        require(isSignatory(msg.sender), "Not a signatory");
        require(!hasSigned[proposalId][msg.sender], "Already signed");

        Proposal storage proposal = proposals[proposalId];
        proposal.signatures++;
        hasSigned[proposalId][msg.sender] = true;

        if (proposal.signatures >= requiredSignatures) {
            executeProposal(proposalId);
        }
    }

    function executeProposal(uint256 proposalId) internal {
        Proposal storage proposal = proposals[proposalId];
        require(proposal.signatures >= requiredSignatures, "Not enough signatures");
        require(!proposal.executed, "Proposal already executed");

        proposal.executed = true;
        proposal.recipient.transfer(proposal.amount);
    }

    function isSignatory(address account) public view returns (bool) {
        for (uint256 i = 0; i < signatories.length; i++) {
            if (signatories[i] == account) {
                return true;
            }
        }
        return false;
    }

    receive() external payable {}
}
