import sqlite3


class EntryRepository:
    def save(self, name, category_id, amount):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO entry(`category_id`, `name`, `amount`) VALUES(?, ?, ?)', (
                    category_id,
                    name,
                    amount
                ))
            connection.commit()


class CategoryRepository:
    def get_by_name(self, name):
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT `id`, `name` FROM category WHERE `name`=?', (name,))

            return cursor.fetchone()
