// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/utils/TokenTimelock.sol";

contract TimelockedERC20 is ERC20, Ownable {
    TokenTimelock public timelock;

    constructor(
        string memory name,
        string memory symbol,
        uint256 initialSupply,
        address beneficiary,
        uint256 releaseTime
    ) ERC20(name, symbol) {
        _mint(msg.sender, initialSupply * (10 ** decimals()));

        // Create a timelock for the beneficiary, specifying the release time
        timelock = new TokenTimelock(this, beneficiary, releaseTime);
    }
}
