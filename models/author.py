from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Author {self.name}>'
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("id must be of int")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if type(value) == str:
            if len(value) > 0:
                if not hasattr(self, '_name'):
                    self._name = value
                else:
                    print("Name cannot be changed after author is instantiated")
            else:
                print("Name must be longer than 0 characters")
        else:
            print("Name must be string")

    @classmethod
    def create(cls, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO authors (name) VALUES (?)
        ''', (name,))
        
        conn.commit()
        author_id = cursor.lastrowid
        conn.close()
        
        return cls(author_id, name)

    @classmethod
    def get_by_id(cls, author_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name FROM authors WHERE id = ?
        ''', (author_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(row['id'], row['name'])
        else:
            return None
        
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT articles.id, articles.title, articles.content
            FROM articles 
            INNER JOIN authors ON articles.author_id = authors.id 
            WHERE authors.id = ?
        ''', (self.id,))

        articles_data = cursor.fetchall()
        conn.close()

        
        return articles_data

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT magazines.id, magazines.name, magazines.category
            FROM magazines 
            INNER JOIN articles ON magazines.id = articles.magazine_id 
            INNER JOIN authors ON articles.author_id = authors.id 
            WHERE authors.id = ?
        ''', (self.id,))

        magazines_data = cursor.fetchall()
        conn.close()

        
        return magazines_data