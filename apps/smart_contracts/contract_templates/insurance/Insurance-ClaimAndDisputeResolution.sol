// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InsuranceWithDisputeResolution {
    struct Claim {
        address claimant;
        uint256 amount;
        bool approved;
        bool disputed;
    }

    mapping(address => Claim[]) public claims;
    address[] public arbitrators;

    event ClaimSubmitted(address indexed claimant, uint256 amount);
    event ClaimDisputed(address indexed claimant, uint256 claimIndex);
    event ClaimApproved(address indexed claimant, uint256 claimIndex, uint256 amount);
    event ClaimDenied(address indexed claimant, uint256 claimIndex);

    function submitClaim(uint256 amount) public {
        claims[msg.sender].push(Claim({
            claimant: msg.sender,
            amount: amount,
            approved: false,
            disputed: false
        }));

        emit ClaimSubmitted(msg.sender, amount);
    }

    function disputeClaim(address claimant, uint256 claimIndex) public {
        require(!claims[claimant][claimIndex].disputed, "Claim already disputed");

        claims[claimant][claimIndex].disputed = true;
        emit ClaimDisputed(claimant, claimIndex);
    }

    function resolveDispute(address claimant, uint256 claimIndex, bool approve) public {
        require(isArbitrator(msg.sender), "Only arbitrators can resolve disputes");

        if (approve) {
            claims[claimant][claimIndex].approved = true;
            payable(claimant).transfer(claims[claimant][claimIndex].amount);
            emit ClaimApproved(claimant, claimIndex, claims[claimant][claimIndex].amount);
        } else {
            emit ClaimDenied(claimant, claimIndex);
        }
    }

    function isArbitrator(address user) public view returns (bool) {
        for (uint256 i = 0; i < arbitrators.length; i++) {
            if (arbitrators[i] == user) {
                return true;
            }
        }
        return false;
    }

    function addArbitrator(address arbitrator) public {
        arbitrators.push(arbitrator);
    }
}
