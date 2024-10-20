// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TokenCuratedRegistryDAO {
    struct Entry {
        string description;
        bool accepted;
        uint256 stakedTokens;
    }

    IERC20 public governanceToken;
    mapping(uint256 => Entry) public registry;
    uint256 public entryCounter;

    uint256 public stakeAmount;

    constructor(address _governanceToken, uint256 _stakeAmount) {
        governanceToken = IERC20(_governanceToken);
        stakeAmount = _stakeAmount;
    }

    function submitEntry(string memory description) public {
        require(governanceToken.balanceOf(msg.sender) >= stakeAmount, "Insufficient stake");

        governanceToken.transferFrom(msg.sender, address(this), stakeAmount);
        registry[entryCounter] = Entry({
            description: description,
            accepted: false,
            stakedTokens: stakeAmount
        });

        entryCounter++;
    }

    function voteEntry(uint256 entryId, bool accept) public {
        require(entryId < entryCounter, "Invalid entry");

        if (accept) {
            registry[entryId].accepted = true;
        } else {
            governanceToken.transfer(msg.sender, registry[entryId].stakedTokens);  // Refund stake if rejected
            delete registry[entryId];
        }
    }
}
