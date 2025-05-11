// Get lawyer ID (replace with actual ID in production)
const lawyerId = 1;

// Fetch and display tasks
async function fetchTasks() {
    const response = await fetch(`/view_tasks/${lawyerId}`);
    const tasks = await response.json();
    const taskList = document.getElementById("taskList");
    taskList.innerHTML = "";
    
    tasks.forEach(task => {
        const taskItem = document.createElement("li");
        taskItem.innerHTML = `
            <span>${task.task_name} - Due: ${task.due_date}</span>
            <button onclick="deleteTask(${task.task_id})">Delete</button>
        `;
        taskList.appendChild(taskItem);
    });
}

// Create a new task
async function createTask() {
    const taskName = document.getElementById("taskName").value;
    const description = document.getElementById("description").value;
    const dueDate = document.getElementById("dueDate").value;

    const response = await fetch('/create_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            lawyer_id: lawyerId,
            task_name: taskName,
            description: description,
            due_date: dueDate
        })
    });

    if (response.ok) {
        alert("Task created successfully!");
        fetchTasks();
    } else {
        alert("Failed to create task.");
    }
}

// Delete a task
async function deleteTask(taskId) {
    const response = await fetch(`/delete_task/${taskId}`, { method: 'DELETE' });
    
    if (response.ok) {
        alert("Task deleted successfully!");
        fetchTasks();
    } else {
        alert("Failed to delete task.");
    }
}

// Load tasks when page loads
document.addEventListener("DOMContentLoaded", fetchTasks);
