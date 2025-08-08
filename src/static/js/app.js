// Main JavaScript file for the todo app

// DOM elements
const todoForm = document.getElementById('todo-form');
const todoInput = document.getElementById('todo-input');
const todoList = document.getElementById('todo-list');

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    console.log('Todo app loaded');
    
    // Load existing todos
    loadTodos();
    
    // Add form submit listener
    if (todoForm) {
        todoForm.addEventListener('submit', addTodo);
    }
});

// Functions
function addTodo(e) {
    e.preventDefault();
    
    const todoText = todoInput.value.trim();
    if (todoText === '') return;
    
    // Add todo logic here
    console.log('Adding todo:', todoText);
    
    // Clear input
    todoInput.value = '';
}

function loadTodos() {
    // Load todos from storage
    console.log('Loading todos...');
}

function deleteTodo(id) {
    // Delete todo logic here
    console.log('Deleting todo:', id);
}

function toggleTodo(id) {
    // Toggle todo completion status
    console.log('Toggling todo:', id);
} 