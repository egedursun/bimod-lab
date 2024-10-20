// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MultiPartyCoordination {
    struct Task {
        string description;
        address assignedParty;
        bool completed;
    }

    Task[] public tasks;

    event TaskCreated(uint256 indexed taskId, string description, address assignedParty);
    event TaskCompleted(uint256 indexed taskId);

    function createTask(string memory description, address assignedParty) public {
        tasks.push(Task({
            description: description,
            assignedParty: assignedParty,
            completed: false
        }));

        emit TaskCreated(tasks.length - 1, description, assignedParty);
    }

    function completeTask(uint256 taskId) public {
        require(msg.sender == tasks[taskId].assignedParty, "Only the assigned party can complete the task");
        require(!tasks[taskId].completed, "Task is already completed");

        tasks[taskId].completed = true;

        emit TaskCompleted(taskId);
    }

    function getTaskStatus(uint256 taskId) public view returns (bool) {
        return tasks[taskId].completed;
    }
}
