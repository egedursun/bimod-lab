// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PropertyAuction {
    address public owner;
    address public highestBidder;
    uint256 public highestBid;
    uint256 public auctionEndTime;
    string public propertyDetails;
    bool public auctionEnded;

    mapping(address => uint256) public pendingReturns;

    event AuctionStarted(string propertyDetails, uint256 auctionEndTime);
    event NewHighestBid(address indexed bidder, uint256 bidAmount);
    event AuctionEnded(address winner, uint256 winningBid);

    constructor(string memory _propertyDetails, uint256 _auctionDuration) {
        owner = msg.sender;
        propertyDetails = _propertyDetails;
        auctionEndTime = block.timestamp + _auctionDuration;
        auctionEnded = false;
    }

    function bid() public payable {
        require(block.timestamp < auctionEndTime, "Auction has ended");
        require(msg.value > highestBid, "There is already a higher bid");

        if (highestBid != 0) {
            pendingReturns[highestBidder] += highestBid;  // Refund the previous highest bidder
        }

        highestBidder = msg.sender;
        highestBid = msg.value;

        emit NewHighestBid(msg.sender, msg.value);
    }

    function withdraw() public {
        uint256 amount = pendingReturns[msg.sender];
        require(amount > 0, "No pending returns");

        pendingReturns[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }

    function endAuction() public {
        require(block.timestamp >= auctionEndTime, "Auction not yet ended");
        require(!auctionEnded, "Auction has already been ended");

        auctionEnded = true;
        emit AuctionEnded(highestBidder, highestBid);

        payable(owner).transfer(highestBid);
    }

    function getAuctionDetails() public view returns (string memory, uint256, address, uint256) {
        return (propertyDetails, auctionEndTime, highestBidder, highestBid);
    }
}
