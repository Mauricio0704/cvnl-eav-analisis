import sqlite3


def create_schema(conn: sqlite3.Connection):
    cursor = conn.cursor()

    cursor.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS questions (
            id TEXT PRIMARY KEY,
            q_text TEXT,
            section TEXT
        );

        
        CREATE TABLE options (
            question_id TEXT NOT NULL,
            option_id INTEGER NOT NULL,
            option_label TEXT NOT NULL,
            PRIMARY KEY (question_id, option_id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        );

        
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY,
            is_initial_respondent BOOLEAN,
            nombre TEXT,
            sexo INTEGER,
            city INTEGER,
            edad_anos INTEGER,
            factor_cvnl REAL,
            grupo_edad TEXT
        );


        CREATE TABLE IF NOT EXISTS answers (
            response_id INTEGER NOT NULL,
            question_id TEXT NOT NULL,
            option_id INTEGER,
            PRIMARY KEY (response_id, question_id),

            FOREIGN KEY (response_id) REFERENCES responses(id),
            FOREIGN KEY (question_id) REFERENCES questions(id),
            FOREIGN KEY (question_id, option_id)
                REFERENCES options(question_id, option_id)
        );

        """
    )

    conn.commit()
