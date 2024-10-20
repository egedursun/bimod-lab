// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract InterestBearingToken is ERC20 {
    uint256 public interestRate;
    uint256 public lastInterestTime;

    event InterestAccrued(address indexed user, uint256 amount);

    constructor(uint256 _initialSupply, uint256 _interestRate) ERC20("InterestBearingToken", "IBT") {
        _mint(msg.sender, _initialSupply);
        interestRate = _interestRate;
        lastInterestTime = block.timestamp;
    }

    function accrueInterest() public {
        uint256 timeElapsed = block.timestamp - lastInterestTime;
        uint256 interest = (totalSupply() * interestRate * timeElapsed) / (365 days * 100);

        _mint(address(this), interest);
        lastInterestTime = block.timestamp;

        emit InterestAccrued(msg.sender, interest);
    }

    function withdrawInterest(uint256 amount) public {
        require(balanceOf(msg.sender) >= amount, "Insufficient balance");

        _burn(msg.sender, amount);
        payable(msg.sender).transfer(amount);
    }

    function getInterestRate() public view returns (uint256) {
        return interestRate;
    }
}
