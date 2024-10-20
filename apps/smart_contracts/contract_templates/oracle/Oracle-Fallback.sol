// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FallbackOracle {
    address public admin;
    address public primaryOracle;
    address public fallbackOracle;
    uint256 public latestValue;

    event ValueUpdated(uint256 value);

    constructor(address _primaryOracle, address _fallbackOracle) {
        admin = msg.sender;
        primaryOracle = _primaryOracle;
        fallbackOracle = _fallbackOracle;
    }

    function updatePrimaryOracle(address newPrimary) public {
        require(msg.sender == admin, "Only admin can update oracle");
        primaryOracle = newPrimary;
    }

    function updateFallbackOracle(address newFallback) public {
        require(msg.sender == admin, "Only admin can update oracle");
        fallbackOracle = newFallback;
    }

    function fetchValue() public {
        (bool success, bytes memory data) = primaryOracle.call(abi.encodeWithSignature("getValue()"));
        if (!success) {
            // Try fallback oracle if primary fails
            (success, data) = fallbackOracle.call(abi.encodeWithSignature("getValue()"));
        }
        require(success, "Both primary and fallback oracles failed");

        latestValue = abi.decode(data, (uint256));
        emit ValueUpdated(latestValue);
    }

    function getValue() public view returns (uint256) {
        return latestValue;
    }
}
