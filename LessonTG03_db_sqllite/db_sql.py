import sqlite3

#Cоздать подключение к базе данных.
conn = sqlite3.connect('bot.db')
#создаем курсор
cursor = conn.cursor()

#теперь можно выполнять действия
#создадим базу данных users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    chat_id INTEGER)''')

#сохраняем изменения
conn.commit()
#закрываем подключение
conn.close()