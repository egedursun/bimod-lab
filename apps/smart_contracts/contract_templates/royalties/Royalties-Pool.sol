// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RoyaltyPool {
    struct Contributor {
        address contributor;
        uint256 sharePercentage;
    }

    Contributor[] public contributors;
    uint256 public totalShares;

    event RoyaltiesDistributed(uint256 totalAmount);

    function addContributor(address _contributor, uint256 _sharePercentage) public {
        contributors.push(Contributor({
            contributor: _contributor,
            sharePercentage: _sharePercentage
        }));
        totalShares += _sharePercentage;
    }

    function distributeRoyalties() public payable {
        require(msg.value > 0, "No royalties to distribute");

        for (uint256 i = 0; i < contributors.length; i++) {
            uint256 amount = (msg.value * contributors[i].sharePercentage) / totalShares;
            payable(contributors[i].contributor).transfer(amount);
        }

        emit RoyaltiesDistributed(msg.value);
    }
}
