class QueryBuilder:
    def __init__(self):
        self._select: list[str] = []
        self._from: str | None = None
        self._joins: list[str] = []
        self._where: list[str] = []
        self._group_by: list[str] = []
        self._order_by: list[str] = []

    def select(self, *columns: str) -> "QueryBuilder":
        self._select.extend(columns)
        return self

    def from_(self, table: str) -> "QueryBuilder":
        self._from = table
        return self

    def join(self, join_sql: str) -> "QueryBuilder":
        self._joins.append(join_sql)
        return self

    def where(self, condition: str) -> "QueryBuilder":
        self._where.append(condition)
        return self

    def group_by(self, *columns: str) -> "QueryBuilder":
        self._group_by.extend(columns)
        return self

    def order_by(self, *columns: str) -> "QueryBuilder":
        self._order_by.extend(columns)
        return self

    def build(self) -> str:
        if not self._select or not self._from:
            raise ValueError("SELECT and FROM are required")

        query = [
            "SELECT",
            "    " + ",\n    ".join(self._select),
            f"FROM {self._from}",
        ]

        if self._joins:
            query.extend(self._joins)

        if self._where:
            query.append("WHERE " + " AND ".join(self._where))

        if self._group_by:
            query.append("GROUP BY " + ", ".join(self._group_by))

        if self._order_by:
            query.append("ORDER BY " + ", ".join(self._order_by))

        return "\n".join(query) + ";"
