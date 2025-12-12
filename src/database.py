import sqlite3
from datetime import datetime


class ResumeDatabase:
    def __init__(self, db_path="resumes.db"):
        self.conn = sqlite3.connect(db_path)
        self.setup_tables()

    def setup_tables(self):
        cursor = self.conn.cursor()

        # table for input data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                education TEXT,
                skills TEXT,
                experience TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')

        # table for generated resume outputs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generated_resumes (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                mode TEXT,
                created_at TEXT
            )
        ''')

        self.conn.commit()

    def save_resume(self, data):
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO resumes (name, email, phone, education, skills, experience, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['email'], data['phone'],
              data['education'], data['skills'], data['experience'], now, now))
        self.conn.commit()
        return cursor.lastrowid

    def load_resume(self, resume_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM resumes WHERE id = ?', (resume_id,))
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0], 'name': row[1], 'email': row[2],
                'phone': row[3], 'education': row[4], 'skills': row[5],
                'experience': row[6]
            }
        return None

    def get_all_resumes(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, updated_at FROM resumes ORDER BY updated_at DESC')
        return cursor.fetchall()

    def save_generated_resume(self, title, content, mode='template'):
        """Save a generated resume output"""
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO generated_resumes (title, content, mode, created_at)
            VALUES (?, ?, ?, ?)
        ''', (title, content, mode, now))
        self.conn.commit()
        return cursor.lastrowid

    def load_generated_resume(self, resume_id):
        """Load a generated resume by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM generated_resumes WHERE id = ?', (resume_id,))
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'mode': row[3],
                'created_at': row[4]
            }
        return None

    def get_all_generated_resumes(self):
        """Get all generated resumes"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, title, created_at FROM generated_resumes ORDER BY created_at DESC')
        return cursor.fetchall()

