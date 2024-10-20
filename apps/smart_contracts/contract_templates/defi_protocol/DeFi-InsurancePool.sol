// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract InsurancePool {
    IERC20 public insuranceToken;
    uint256 public totalCoverage;

    struct Claim {
        address claimant;
        uint256 amount;
        bool approved;
        bool paidOut;
    }

    mapping(uint256 => Claim) public claims;
    uint256 public claimCount;

    event CoverageProvided(address indexed provider, uint256 amount);
    event ClaimSubmitted(address indexed claimant, uint256 amount);
    event ClaimPaid(address indexed claimant, uint256 amount);

    constructor(IERC20 _insuranceToken) {
        insuranceToken = _insuranceToken;
    }

    function provideCoverage(uint256 amount) public {
        require(amount > 0, "Coverage amount must be greater than 0");

        insuranceToken.transferFrom(msg.sender, address(this), amount);
        totalCoverage += amount;

        emit CoverageProvided(msg.sender, amount);
    }

    function submitClaim(uint256 amount) public {
        require(amount > 0 && amount <= totalCoverage, "Invalid claim amount");

        claims[claimCount] = Claim({
            claimant: msg.sender,
            amount: amount,
            approved: false,
            paidOut: false
        });
        claimCount++;

        emit ClaimSubmitted(msg.sender, amount);
    }

    function approveClaim(uint256 claimId) public {
        Claim storage claim = claims[claimId];
        require(!claim.approved, "Claim already approved");

        claim.approved = true;
    }

    function payoutClaim(uint256 claimId) public {
        Claim storage claim = claims[claimId];
        require(claim.approved, "Claim not approved");
        require(!claim.paidOut, "Claim already paid");

        insuranceToken.transfer(claim.claimant, claim.amount);
        totalCoverage -= claim.amount;
        claim.paidOut = true;

        emit ClaimPaid(claim.claimant, claim.amount);
    }
}
