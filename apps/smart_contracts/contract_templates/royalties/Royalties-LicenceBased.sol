// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LicenseRoyalties {
    address public licensor;
    mapping(address => uint256) public licenseFees;
    mapping(address => uint256) public licenseDurations;

    event LicenseGranted(address indexed licensee, uint256 fee, uint256 duration);
    event RoyaltiesPaid(address indexed licensee, uint256 amount);

    constructor() {
        licensor = msg.sender;
    }

    function grantLicense(address licensee, uint256 fee, uint256 duration) public {
        require(msg.sender == licensor, "Only the licensor can grant licenses");

        licenseFees[licensee] = fee;
        licenseDurations[licensee] = block.timestamp + duration;

        emit LicenseGranted(licensee, fee, duration);
    }

    function payLicenseFee() public payable {
        require(msg.value == licenseFees[msg.sender], "Incorrect license fee");
        require(block.timestamp <= licenseDurations[msg.sender], "License expired");

        payable(licensor).transfer(msg.value);

        emit RoyaltiesPaid(msg.sender, msg.value);
    }

    function checkLicenseStatus(address licensee) public view returns (bool) {
        return block.timestamp <= licenseDurations[licensee];
    }
}
