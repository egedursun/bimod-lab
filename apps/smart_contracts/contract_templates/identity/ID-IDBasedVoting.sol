// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IdentityVoting {
    mapping(address => bool) public verifiedVoters;
    mapping(uint256 => uint256) public proposals;
    mapping(address => bool) public voted;

    event VoterVerified(address indexed voter);
    event Voted(address indexed voter, uint256 indexed proposalId);

    function verifyVoter(address voter) public {
        // Verifier is assumed to be an admin or a decentralized authority
        verifiedVoters[voter] = true;
        emit VoterVerified(voter);
    }

    function vote(uint256 proposalId) public {
        require(verifiedVoters[msg.sender], "Not a verified voter");
        require(!voted[msg.sender], "Already voted");

        proposals[proposalId] += 1;
        voted[msg.sender] = true;

        emit Voted(msg.sender, proposalId);
    }

    function getProposalVotes(uint256 proposalId) public view returns (uint256) {
        return proposals[proposalId];
    }
}
