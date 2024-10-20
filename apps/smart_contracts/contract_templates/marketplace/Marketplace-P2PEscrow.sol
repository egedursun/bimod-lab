// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract P2PMarketplace {
    struct Escrow {
        address buyer;
        address seller;
        uint256 amount;
        bool isCompleted;
    }

    mapping(uint256 => Escrow) public escrows;
    uint256 public escrowCount;

    event EscrowCreated(address indexed buyer, address indexed seller, uint256 indexed escrowId, uint256 amount);
    event EscrowCompleted(uint256 indexed escrowId, uint256 amount);

    function createEscrow(address seller) public payable {
        require(msg.value > 0, "Escrow amount must be greater than 0");

        escrows[escrowCount] = Escrow({
            buyer: msg.sender,
            seller: seller,
            amount: msg.value,
            isCompleted: false
        });
        escrowCount++;

        emit EscrowCreated(msg.sender, seller, escrowCount - 1, msg.value);
    }

    function completeEscrow(uint256 escrowId) public {
        Escrow storage escrow = escrows[escrowId];
        require(msg.sender == escrow.buyer || msg.sender == escrow.seller, "Only buyer or seller can complete escrow");
        require(!escrow.isCompleted, "Escrow already completed");

        escrow.isCompleted = true;
        payable(escrow.seller).transfer(escrow.amount);

        emit EscrowCompleted(escrowId, escrow.amount);
    }
}
