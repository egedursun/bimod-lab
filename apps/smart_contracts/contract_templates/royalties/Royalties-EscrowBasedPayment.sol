// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EscrowRoyalties {
    address public creator;
    uint256 public milestone;
    uint256 public fundsHeld;
    uint256 public totalSales;

    event FundsReleased(address indexed creator, uint256 amount);

    constructor(uint256 _milestone) {
        creator = msg.sender;
        milestone = _milestone;
        fundsHeld = 0;
    }

    function depositFunds() public payable {
        fundsHeld += msg.value;
    }

    function recordSale(uint256 saleAmount) public {
        totalSales += saleAmount;
        fundsHeld += saleAmount;

        if (totalSales >= milestone) {
            releaseFunds();
        }
    }

    function releaseFunds() private {
        require(fundsHeld > 0, "No funds to release");

        payable(creator).transfer(fundsHeld);
        emit FundsReleased(creator, fundsHeld);

        fundsHeld = 0;  // Reset funds held
    }
}
