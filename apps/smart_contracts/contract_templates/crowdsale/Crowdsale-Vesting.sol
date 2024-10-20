// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract VestingCrowdsale is Ownable {
    IERC20 public token;
    address payable public wallet;
    uint256 public rate;
    uint256 public weiRaised;

    struct VestingSchedule {
        uint256 releaseTime;
        uint256 amount;
    }

    mapping(address => VestingSchedule[]) public vestingSchedules;

    constructor(uint256 _rate, address payable _wallet, IERC20 _token) {
        require(_rate > 0, "Rate must be greater than 0");
        require(_wallet != address(0), "Invalid wallet address");
        require(address(_token) != address(0), "Invalid token address");

        rate = _rate;
        wallet = _wallet;
        token = _token;
    }

    function buyTokens() public payable {
        uint256 weiAmount = msg.value;
        require(weiAmount > 0, "Ether amount is 0");

        uint256 tokens = weiAmount * rate;
        weiRaised += weiAmount;

        // Define vesting schedule (e.g., 50% after 1 month, 50% after 3 months)
        vestingSchedules[msg.sender].push(VestingSchedule({
            releaseTime: block.timestamp + 30 days,
            amount: tokens / 2
        }));
        vestingSchedules[msg.sender].push(VestingSchedule({
            releaseTime: block.timestamp + 90 days,
            amount: tokens / 2
        }));

        wallet.transfer(msg.value);  // Forward Ether to the wallet
    }

    function claimTokens() public {
        uint256 totalClaimed = 0;

        for (uint256 i = 0; i < vestingSchedules[msg.sender].length; i++) {
            VestingSchedule storage schedule = vestingSchedules[msg.sender][i];

            if (block.timestamp >= schedule.releaseTime && schedule.amount > 0) {
                totalClaimed += schedule.amount;
                schedule.amount = 0;
            }
        }

        require(totalClaimed > 0, "No tokens available for claim");
        token.transfer(msg.sender, totalClaimed);
    }
}
