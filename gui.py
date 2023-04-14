import functions
import PySimpleGUI
import time
import os

if not os.path.exists("todos.txt"):
    with open("todos.txt", "w") as file:
        pass

PySimpleGUI.theme("DarkPurple3")

Clock = PySimpleGUI.Text("", key='clock')
label = PySimpleGUI.Text("Type your To-Do item: ")
input_box = PySimpleGUI.InputText(tooltip="Enter to-do", key="todo")
add_button = PySimpleGUI.Button(size=4, image_source="add.png",
                                tooltip="Add Todo", key="Add")
list_box = PySimpleGUI.Listbox(values=functions.get_todos(),
                               key='todos',
                               enable_events=True, size=[45, 10])

edit_button = PySimpleGUI.Button('Edit')
complete_button = PySimpleGUI.Button(size=4, image_source="complete.png",
                                     tooltip="Remove completed todo", key="Complete")
exit_button = PySimpleGUI.Button('Exit')

window = PySimpleGUI.Window('My To-DO App',
                            layout=[[Clock],
                                    [label],
                                    [input_box, add_button],
                                    [list_box, edit_button, complete_button],
                                    [exit_button]],
                            font=('Ariel', 20))

while True:
    """ values and event lists to todos app and values is the values in the lists like hash mapas"""
    event,  values = window.read(timeout=200)
    window["clock"].update(value=time.strftime('%B %d, %Y %H:%M:%S'))

    match event:
        case 'Add':
            todos = functions.get_todos()
            new_todo = values['todo'] + "\n"

            todos.append(new_todo)

            functions.write_todos(todos)
            window['todos'].update(values=todos)

        case 'Edit':
            try:
                todo_to_edit = values['todos'][0]
                new_todo = PySimpleGUI.popup_get_text('Edit Todo', default_text=todo_to_edit)
                if new_todo:  # check if user entered new text
                    todos = functions.get_todos()
                    index = todos.index(todo_to_edit)
                    todos[index] = new_todo + '\n'
                    functions.write_todos(todos)
                    window['todos'].update(values=todos)
            except IndexError:
                PySimpleGUI.popup("Please select an item first", font=("Ariel", 25))

        case 'Complete':
            try:
                todo_to_complete = values['todos'][0]
                todos = functions.get_todos()
                todos.remove(todo_to_complete)
                functions.write_todos(todos)
                window['todos'].update(values=todos)
                window['todo'].update(value="")
            except IndexError:
                PySimpleGUI.popup("Please select an item first", font=("Ariel", 25))

        case 'Exit':
            break

        case 'todos':
            window['todo'].update(value=values['todos'][0])

        case PySimpleGUI.WIN_CLOSED:
            break

window.close()


