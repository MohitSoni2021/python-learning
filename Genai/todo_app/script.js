const addTodoBtn = document.getElementById("addTodoBtn");
const newTodoInput = document.getElementById("newTodo");
const todoList = document.getElementById("todos");

addTodoBtn.addEventListener("click", () => {
  const newTodoText = newTodoInput.value;
  if (newTodoText) {
    const newTodo = document.createElement("li");
    newTodo.textContent = newTodoText;
    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "X";
    deleteBtn.addEventListener("click", () => {
      todoList.removeChild(newTodo);
    });
    newTodo.appendChild(deleteBtn);
    todoList.appendChild(newTodo);
    newTodoInput.value = "";
  }
});

