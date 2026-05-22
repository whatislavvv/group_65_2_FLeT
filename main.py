import flet as ft 
from db import main_db

def main_page(page: ft.Page):
    page.title = 'ToDo List'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=20, scroll=ft.ScrollMode.AUTO, expand=True) 

    filter_type = 'all'
    
    def load_tasks():
        task_list.controls.clear()
        for task_id, task, completed in main_db.get_tasks(filter_type):
            task_list.controls.append(view_task(task_id=task_id, task_text=task, completed=completed))
        page.update()

    def view_task(task_id, task_text, completed=0):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)

        checkbox = ft.Checkbox(value=bool(completed), on_change=lambda e: toggle_task(task_id=task_id, is_completed=e.control.value))

        def save_edit(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            page.update()

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_edit)

        def enable_edit(_):
            if task_field.read_only == True:
                task_field.read_only = False
            else:
                task_field.read_only = True
            page.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def delete_click(_):
            main_db.delete_task(task_id=task_id) 
            load_tasks()

        delete_button = ft.IconButton(
            icon=ft.Icons.DELETE, 
            icon_color=ft.Colors.RED,
            on_click=delete_click
        )
        
        return ft.Row([checkbox, task_field, edit_button, save_button, delete_button])
    
    def toggle_task(task_id, is_completed):
        print(is_completed)
        main_db.update_task(task_id=task_id, completed=int(is_completed))
        print(int(is_completed))
        load_tasks()

    def add_task_flet(_):
        if task_input.value:
            task_text = task_input.value.strip()
            main_db.add_task(task=task_text)
            task_input.value = None
            load_tasks()

    task_input = ft.TextField(label='Введите задачу', on_submit=add_task_flet)

    def set_filter(filter_value):
        nonlocal filter_type
        print(filter_type)
        filter_type = filter_value
        print(filter_type)
        load_tasks()

    filter_buttons = ft.Row([
        ft.ElevatedButton('Все задачи', on_click=lambda e: set_filter('all')),
        ft.ElevatedButton('В работе', on_click=lambda e: set_filter('uncompleted')),
        ft.ElevatedButton('Готово', on_click=lambda e: set_filter('completed'))
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

    def delete_completed(_):
        main_db.delete_all_completed()
        load_tasks()

    clear_button = ft.ElevatedButton('Очистить выполненные', on_click=delete_completed, bgcolor=ft.Colors.RED_200)
    page.add(task_input, filter_buttons, clear_button, task_list)
    load_tasks()

if __name__ == '__main__':
    main_db.init_db()
    ft.app(main_page)