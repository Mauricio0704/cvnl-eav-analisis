def get_question_sections_query() -> str:
    query = """
        SELECT DISTINCT
            section
        FROM questions
        WHERE section IS NOT NULL
        ORDER BY section;
    """
    return query


def get_questions_by_section_query(section: str) -> str:
    query = f"""
        SELECT
            id,
            q_text
        FROM questions
        WHERE section = '{section}'
        ORDER BY id;
    """
    return query
