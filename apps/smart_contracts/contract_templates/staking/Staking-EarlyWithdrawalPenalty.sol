// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract EarlyWithdrawalPenaltyStaking {
    IERC20 public stakingToken;
    uint256 public lockDuration;
    uint256 public penaltyPercentage;  // E.g., 10 means 10% penalty

    struct Stake {
        uint256 amount;
        uint256 startTime;
    }

    mapping(address => Stake) public stakes;

    constructor(IERC20 _stakingToken, uint256 _lockDuration, uint256 _penaltyPercentage) {
        stakingToken = _stakingToken;
        lockDuration = _lockDuration;
        penaltyPercentage = _penaltyPercentage;
    }

    function stake(uint256 amount) public {
        require(amount > 0, "Cannot stake 0 tokens");

        stakingToken.transferFrom(msg.sender, address(this), amount);
        stakes[msg.sender] = Stake({
            amount: amount,
            startTime: block.timestamp
        });
    }

    function withdraw() public {
        Stake storage stakeInfo = stakes[msg.sender];
        uint256 timeStaked = block.timestamp - stakeInfo.startTime;

        uint256 penalty = 0;
        if (timeStaked < lockDuration) {
            penalty = (stakeInfo.amount * penaltyPercentage) / 100;
        }

        uint256 amountToTransfer = stakeInfo.amount - penalty;
        stakeInfo.amount = 0;
        stakingToken.transfer(msg.sender, amountToTransfer);
    }
}
