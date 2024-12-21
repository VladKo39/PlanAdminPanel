import sqlite3
import create_data
disc_prod=create_data.create_data_bot()

def initiate_db():
    # создаёт таблицу Products, если она ещё не создана при помощи SQL запроса.
    connection = sqlite3.connect('data_bot.db')
    # подключение к базе данных not_telegram.db с помощью библиотеки sqlite3
    cursor = connection.cursor()
    # создаю объект cursor для выполнения SQL-запросов и операций с базой данных.

    cursor.execute('''                            
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY ,
    title TEXT INTEGER NOT NULL,
    description TEXT ,
    price INTEGER NOT NULL
    );
    ''')

    cursor.execute('''       
            DELETE FROM Products
            ''')

    # для заполнения данных таблицы Products очищаю её
    create_data.create_data_bot()
    # вызываю функцию подготовки данных для загрузки в таблицу Products

    for key, value in disc_prod.items():
        # для перебора элементов словаря disc_prod с данными
        title_ = value[0]
        description_ = value[1]
        price_ = value[2]
        cursor.execute('INSERT INTO Products('
                       'title,'
                       'description,'
                       'price) '
                       ' VALUES(?,?,?)',
                       (title_,
                        description_,
                        price_
                        )
                       )
        # заполняю таблицу Products данными из словаря

    connection.commit()
    # сохраняем изменения
    connection.close()
    # отключаем подключение

def get_all_products():
    connection = sqlite3.connect('data_bot.db')
    # # подключение к базе данных not_telegram.db с помощью библиотеки sqlite3
    cursor = connection.cursor()
    # # создаю объект cursor для выполнения SQL-запросов и операций с базой данных.

    cursor.execute("SELECT * FROM Products")
    return cursor.fetchall()
    connection.close()
    # отключаем подключение


if __name__ == '__main__':
    initiate_db()
    get_all_products()

