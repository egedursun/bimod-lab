// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SupplyChainFinancing {
    struct Loan {
        address financier;
        address supplier;
        uint256 loanAmount;
        uint256 repaymentAmount;
        uint256 dueDate;
        bool repaid;
    }

    Loan[] public loans;

    event LoanIssued(address indexed financier, address indexed supplier, uint256 loanAmount);
    event LoanRepaid(address indexed supplier, uint256 repaymentAmount);

    function issueLoan(address supplier, uint256 loanAmount, uint256 repaymentAmount, uint256 dueDate) public {
        loans.push(Loan({
            financier: msg.sender,
            supplier: supplier,
            loanAmount: loanAmount,
            repaymentAmount: repaymentAmount,
            dueDate: dueDate,
            repaid: false
        }));

        payable(supplier).transfer(loanAmount);

        emit LoanIssued(msg.sender, supplier, loanAmount);
    }

    function repayLoan(uint256 loanId) public payable {
        require(msg.sender == loans[loanId].supplier, "Only the supplier can repay the loan");
        require(msg.value == loans[loanId].repaymentAmount, "Incorrect repayment amount");
        require(!loans[loanId].repaid, "Loan already repaid");

        loans[loanId].repaid = true;
        payable(loans[loanId].financier).transfer(msg.value);

        emit LoanRepaid(msg.sender, msg.value);
    }

    function getLoanDetails(uint256 loanId) public view returns (address, uint256, uint256, uint256, bool) {
        Loan memory loan = loans[loanId];
        return (loan.supplier, loan.loanAmount, loan.repaymentAmount, loan.dueDate, loan.repaid);
    }
}
