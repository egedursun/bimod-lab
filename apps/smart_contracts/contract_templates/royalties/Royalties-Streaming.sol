// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract StreamingRoyalties {
    address public creator;
    uint256 public royaltyPerStream;
    mapping(address => uint256) public streams;

    event StreamPaid(address indexed streamer, uint256 streamsPaid);

    constructor(uint256 _royaltyPerStream) {
        creator = msg.sender;
        royaltyPerStream = _royaltyPerStream;
    }

    function payForStream(uint256 streamCount) public payable {
        require(msg.value == streamCount * royaltyPerStream, "Incorrect payment amount");

        streams[msg.sender] += streamCount;
        payable(creator).transfer(msg.value);

        emit StreamPaid(msg.sender, streamCount);
    }

    function getStreamCount(address streamer) public view returns (uint256) {
        return streams[streamer];
    }
}
