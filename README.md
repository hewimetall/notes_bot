# Данный бот нужен для ведения заметок и задач на день.
Команды

/create_note <tag>
/create_task
/list_task
/list_note
/get_note <id>
/kill_note <id>
/kill_task <id>

# Task 
Создается в директории date/TASK.md.
Формат файла md.
```md
* Поел
* Поспал
* Сохраниться
```
<id> = номеру строки

# Notion
Создается в директории data/<tag>.md.
Обновляется полностью