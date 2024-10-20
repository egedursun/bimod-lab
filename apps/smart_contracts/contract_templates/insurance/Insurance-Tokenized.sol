// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract TokenizedInsurancePool is ERC20 {
    uint256 public poolBalance;

    event PoolTokenMinted(address indexed user, uint256 amount);
    event ClaimPaid(address indexed policyholder, uint256 payoutAmount);

    constructor() ERC20("InsurancePoolToken", "IPT") {}

    function mintPoolTokens() public payable {
        require(msg.value > 0, "Must contribute to pool");
        uint256 tokenAmount = msg.value;

        _mint(msg.sender, tokenAmount);
        poolBalance += msg.value;

        emit PoolTokenMinted(msg.sender, tokenAmount);
    }

    function payClaim(address policyholder, uint256 payoutAmount) public {
        require(poolBalance >= payoutAmount, "Insufficient pool balance");

        poolBalance -= payoutAmount;
        payable(policyholder).transfer(payoutAmount);

        emit ClaimPaid(policyholder, payoutAmount);
    }

    function getPoolBalance() public view returns (uint256) {
        return poolBalance;
    }
}
