// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LeaseToOwn {
    address public landlord;
    address public tenant;
    uint256 public leasePrice;
    uint256 public propertyValue;
    uint256 public paidAmount;
    bool public leaseActive;

    event LeaseStarted(address indexed tenant, uint256 leasePrice);
    event PaymentMade(address indexed tenant, uint256 amount);
    event OwnershipTransferred(address indexed tenant);

    constructor(uint256 _leasePrice, uint256 _propertyValue) {
        landlord = msg.sender;
        leasePrice = _leasePrice;
        propertyValue = _propertyValue;
        paidAmount = 0;
        leaseActive = true;
    }

    function startLease(address _tenant) public {
        require(msg.sender == landlord, "Only landlord can start lease");
        tenant = _tenant;
        emit LeaseStarted(tenant, leasePrice);
    }

    function makePayment() public payable {
        require(msg.sender == tenant, "Only tenant can make payments");
        require(msg.value == leasePrice, "Incorrect payment amount");
        require(leaseActive, "Lease is no longer active");

        paidAmount += msg.value;
        emit PaymentMade(tenant, msg.value);

        if (paidAmount >= propertyValue) {
            leaseActive = false;
            emit OwnershipTransferred(tenant);
        }
    }
}
