// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract PeerToPeerLending {
    struct LoanRequest {
        address borrower;
        uint256 collateralAmount;
        uint256 loanAmount;
        uint256 interestRate;
        uint256 loanDueDate;
        bool active;
    }

    struct LoanOffer {
        address lender;
        uint256 loanAmount;
        uint256 interestRate;
        bool active;
    }

    IERC20 public collateralToken;
    IERC20 public loanToken;

    mapping(address => LoanRequest) public loanRequests;
    mapping(address => LoanOffer) public loanOffers;

    event LoanRequested(address indexed borrower, uint256 loanAmount, uint256 collateralAmount, uint256 interestRate);
    event LoanOffered(address indexed lender, uint256 loanAmount, uint256 interestRate);
    event LoanMatched(address indexed borrower, address indexed lender, uint256 loanAmount, uint256 collateralAmount, uint256 interestRate);

    constructor(IERC20 _collateralToken, IERC20 _loanToken) {
        collateralToken = _collateralToken;
        loanToken = _loanToken;
    }

    function requestLoan(uint256 collateralAmount, uint256 loanAmount, uint256 interestRate, uint256 duration) public {
        require(collateralAmount > 0 && loanAmount > 0, "Amounts must be greater than 0");
        require(interestRate > 0 && duration > 0, "Interest rate and duration must be greater than 0");

        collateralToken.transferFrom(msg.sender, address(this), collateralAmount);

        loanRequests[msg.sender] = LoanRequest({
            borrower: msg.sender,
            collateralAmount: collateralAmount,
            loanAmount: loanAmount,
            interestRate: interestRate,
            loanDueDate: block.timestamp + duration,
            active: true
        });

        emit LoanRequested(msg.sender, loanAmount, collateralAmount, interestRate);
    }

    function offerLoan(uint256 loanAmount, uint256 interestRate) public {
        require(loanAmount > 0 && interestRate > 0, "Loan amount and interest rate must be greater than 0");

        loanOffers[msg.sender] = LoanOffer({
            lender: msg.sender,
            loanAmount: loanAmount,
            interestRate: interestRate,
            active: true
        });

        emit LoanOffered(msg.sender, loanAmount, interestRate);
    }

    function matchLoan(address borrower, address lender) public {
        LoanRequest storage request = loanRequests[borrower];
        LoanOffer storage offer = loanOffers[lender];

        require(request.active && offer.active, "Loan request or offer is not active");
        require(offer.loanAmount == request.loanAmount, "Loan amounts do not match");
        require(offer.interestRate == request.interestRate, "Interest rates do not match");

        loanToken.transferFrom(lender, borrower, request.loanAmount);
        request.active = false;
        offer.active = false;

        emit LoanMatched(borrower, lender, request.loanAmount, request.collateralAmount, request.interestRate);
    }
}
