
const inputTask = document.getElementById('inputTask');
const taskList = document.getElementById('taskList');
const API_URL = "http://127.0.0.1:5000/tasks";


window.onload = fetchTasks;

function fetchTasks() {
  fetch(API_URL)
    .then(res => res.json())
    .then(tasks => {
      taskList.innerHTML = '';
      tasks.forEach(task => renderTask(task));
    });
}

function renderTask(task) {
  const li = document.createElement('li');

  const checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.checked = task.completed;
  checkbox.onchange = () => updateTask(task.id, checkbox.checked);

  const span = document.createElement('span');
  span.textContent = task.text;   ✅ using 'text'

  const deleteBtn = document.createElement('button');
  deleteBtn.textContent = '❌';
  deleteBtn.onclick = () => deleteTask(task.id);

  li.appendChild(checkbox);
  li.appendChild(span);
  li.appendChild(deleteBtn);

  taskList.appendChild(li);
}

function addTask() {
  const text = inputTask.value.trim();
  if (!text) return;

  fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })   ✅ using 'text'
  }).then(res => {
    if (res.ok) {
      inputTask.value = '';
      fetchTasks();  
    }
  });
}

function updateTask(id, completed) {
  fetch(${API_URL}/${id}, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ completed })
  }).then(fetchTasks);
}

function deleteTask(id) {
  fetch(${API_URL}/${id}, {
    method: 'DELETE'
  }).then(fetchTasks);
}