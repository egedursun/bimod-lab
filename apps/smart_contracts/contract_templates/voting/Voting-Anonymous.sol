// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AnonymousVoting {
    struct Voter {
        bytes32 voteHash;
        bool hasVoted;
        bool hasRevealed;
        uint8 vote;
    }

    mapping(address => Voter) public voters;
    uint256 public revealEndTime;
    uint256 public commitEndTime;
    uint256 public votesFor;
    uint256 public votesAgainst;

    event VoteCommitted(address indexed voter);
    event VoteRevealed(address indexed voter, uint8 vote);

    constructor(uint256 _commitDuration, uint256 _revealDuration) {
        commitEndTime = block.timestamp + _commitDuration;
        revealEndTime = block.timestamp + _commitDuration + _revealDuration;
    }

    function commitVote(bytes32 voteHash) public {
        require(block.timestamp <= commitEndTime, "Commit phase has ended");
        require(!voters[msg.sender].hasVoted, "Already committed a vote");

        voters[msg.sender] = Voter({
            voteHash: voteHash,
            hasVoted: true,
            hasRevealed: false,
            vote: 0
        });

        emit VoteCommitted(msg.sender);
    }

    function revealVote(uint8 vote, string memory secret) public {
        require(block.timestamp > commitEndTime, "Commit phase not ended");
        require(block.timestamp <= revealEndTime, "Reveal phase has ended");
        require(voters[msg.sender].hasVoted, "No vote to reveal");
        require(!voters[msg.sender].hasRevealed, "Already revealed");

        bytes32 voteHash = keccak256(abi.encodePacked(vote, secret));
        require(voteHash == voters[msg.sender].voteHash, "Vote hash mismatch");

        voters[msg.sender].vote = vote;
        voters[msg.sender].hasRevealed = true;

        if (vote == 1) {
            votesFor++;
        } else {
            votesAgainst++;
        }

        emit VoteRevealed(msg.sender, vote);
    }
}
