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
            respondent_id TEXT PRIMARY KEY,
            is_initial_respondent BOOLEAN,
            nombre TEXT,
            sexo INTEGER,
            city INTEGER,
            edad_anos INTEGER,
            factor_cvnl REAL,
            grupo_edad TEXT
        );


        CREATE TABLE IF NOT EXISTS answers (
            respondent_id TEXT NOT NULL,
            question_id TEXT NOT NULL,
            option_id INTEGER,
            value REAL,

            PRIMARY KEY (respondent_id, question_id),

            FOREIGN KEY (respondent_id) REFERENCES responses(respondent_id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
            
            CHECK (
                (option_id IS NOT NULL AND value IS NULL) OR
                (option_id IS NULL AND value IS NOT NULL)
            )
        );

        CREATE TABLE IF NOT EXISTS respondent_attributes (
            respondent_id TEXT NOT NULL,
            question_id TEXT NOT NULL,
            attribute TEXT NOT NULL,
            value INTEGER NOT NULL,
            PRIMARY KEY (respondent_id, attribute),
            FOREIGN KEY (respondent_id) REFERENCES responses(respondent_id)
        );

        """
    )

    conn.commit()
