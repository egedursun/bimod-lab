// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RentalAgreement {
    address public landlord;
    address public tenant;
    uint256 public rentAmount;
    uint256 public securityDeposit;
    uint256 public rentDueDate;
    bool public isActive;

    event RentPaid(address indexed tenant, uint256 amount);
    event LeaseTerminated(address indexed tenant);

    constructor(address _tenant, uint256 _rentAmount, uint256 _securityDeposit) {
        landlord = msg.sender;
        tenant = _tenant;
        rentAmount = _rentAmount;
        securityDeposit = _securityDeposit;
        isActive = true;
    }

    function payRent() public payable {
        require(msg.sender == tenant, "Only the tenant can pay rent");
        require(msg.value == rentAmount, "Incorrect rent amount");
        require(isActive, "Lease is no longer active");

        rentDueDate += 30 days;  // Rent is due every 30 days
        emit RentPaid(tenant, msg.value);
    }

    function terminateLease() public {
        require(msg.sender == landlord || msg.sender == tenant, "Only landlord or tenant can terminate the lease");

        isActive = false;
        payable(tenant).transfer(securityDeposit);  // Return security deposit to tenant

        emit LeaseTerminated(tenant);
    }
}
