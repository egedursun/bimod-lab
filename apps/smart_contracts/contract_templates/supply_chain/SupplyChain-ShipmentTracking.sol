// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ShipmentTracking {
    struct Shipment {
        string origin;
        string destination;
        string currentLocation;
        bool isDelivered;
    }

    mapping(uint256 => Shipment) public shipments;

    event ShipmentCreated(uint256 indexed shipmentId, string origin, string destination);
    event ShipmentUpdated(uint256 indexed shipmentId, string newLocation);
    event ShipmentDelivered(uint256 indexed shipmentId);

    function createShipment(uint256 shipmentId, string memory origin, string memory destination) public {
        require(bytes(shipments[shipmentId].origin).length == 0, "Shipment already exists");

        shipments[shipmentId] = Shipment({
            origin: origin,
            destination: destination,
            currentLocation: origin,
            isDelivered: false
        });

        emit ShipmentCreated(shipmentId, origin, destination);
    }

    function updateShipmentLocation(uint256 shipmentId, string memory newLocation) public {
        require(!shipments[shipmentId].isDelivered, "Shipment is already delivered");

        shipments[shipmentId].currentLocation = newLocation;

        emit ShipmentUpdated(shipmentId, newLocation);
    }

    function markShipmentDelivered(uint256 shipmentId) public {
        require(!shipments[shipmentId].isDelivered, "Shipment is already delivered");

        shipments[shipmentId].isDelivered = true;

        emit ShipmentDelivered(shipmentId);
    }

    function getShipmentDetails(uint256 shipmentId) public view returns (string memory, string memory, string memory, bool) {
        Shipment memory shipment = shipments[shipmentId];
        return (shipment.origin, shipment.destination, shipment.currentLocation, shipment.isDelivered);
    }
}
