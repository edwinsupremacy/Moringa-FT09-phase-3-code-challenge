from database.connection import get_db_connection

class Article:
    def __init__(self, author, magazine, title, content):
        self.author = author
        self.magazine = magazine
        self.title = title
        self.content = content
        self._insert_into_db()

    def __repr__(self):
        return f'<Article {self.title}>'
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise ValueError("Title must be a string")
        if not 5 <= len(value) <= 50:
            raise ValueError("Title must be between 5 and 50 characters inclusive")
        if hasattr(self, '_title'):
            raise AttributeError("Title cannot be changed after the article is instantiated")
        self._title = value

    
    def _insert_into_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)
        ''', (self.title, self.content, self.author.id, self.magazine.id))
        
        conn.commit()
        conn.close()

    def get_author(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT authors.name FROM articles 
            INNER JOIN authors ON articles.author_id = authors.id 
            WHERE articles.id = ?
        ''', (self.id,))
        
        author_name = cursor.fetchone()[0]
        conn.close()
        return author_name

    def get_magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT magazines.name FROM articles 
            INNER JOIN magazines ON articles.magazine_id = magazines.id 
            WHERE articles.id = ?
        ''', (self.id,))
        
        magazine_name = cursor.fetchone()[0]
        conn.close()
        return magazine_name

    author_name = property(get_author)
    magazine_name = property(get_magazine)

    