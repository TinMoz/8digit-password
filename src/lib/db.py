from typing import List, Optional, Tuple

from sqlalchemy import bindparam, create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import make_url


class RandomNumberStore:
    def __init__(self, db_url: str):
        url = make_url(str(db_url))
        connect_args = {}
        if url.get_backend_name() in {"mysql", "mariadb"}:
            connect_args = {"ssl": {"ssl": {}}}

        self.engine: Engine = create_engine(url, connect_args=connect_args)

    def _schema(self) -> str:
        if self.engine.url.get_backend_name() == "sqlite":
            return """
            CREATE TABLE IF NOT EXISTS random_numbers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value TEXT NOT NULL,
                viewed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """

        return """
        CREATE TABLE IF NOT EXISTS random_numbers (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            value VARCHAR(255) NOT NULL,
            viewed TINYINT(1) NOT NULL DEFAULT 0,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """

    def _has_viewed_column(self, conn) -> bool:
        dialect = self.engine.url.get_backend_name()
        if dialect == "sqlite":
            rows = conn.execute(text("PRAGMA table_info(random_numbers)")).fetchall()
            return any(row[1] == "viewed" for row in rows)

        result = conn.execute(
            text(
                """
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = :schema
                  AND TABLE_NAME = 'random_numbers'
                  AND COLUMN_NAME = 'viewed'
                """
            ),
            {"schema": self.engine.url.database},
        ).scalar_one()
        return result > 0

    def _ensure_viewed_column(self, conn) -> None:
        if self._has_viewed_column(conn):
            return

        if self.engine.url.get_backend_name() == "sqlite":
            conn.execute(
                text("ALTER TABLE random_numbers ADD COLUMN viewed INTEGER NOT NULL DEFAULT 0")
            )
        else:
            conn.execute(
                text("ALTER TABLE random_numbers ADD COLUMN viewed TINYINT(1) NOT NULL DEFAULT 0")
            )

    def initialize(self) -> None:
        """初始化表结构并确保 viewed 列存在"""
        with self.engine.begin() as conn:
            conn.execute(text(self._schema()))
            self._ensure_viewed_column(conn)

    def insert_number(self, number: str) -> None:
        """插入一个随机数字（未读）"""
        with self.engine.begin() as conn:
            conn.execute(
                text("INSERT INTO random_numbers (value, viewed) VALUES (:value, 0)"),
                {"value": number},
            )

    def fetch_numbers(self, limit: Optional[int] = None, include_viewed: bool = True) -> List[str]:
        """按 id 倒序取出数字列表，可选择过滤已读"""
        sql = "SELECT value FROM random_numbers"
        params = {}
        if not include_viewed:
            sql += " WHERE viewed = 0"

        sql += " ORDER BY id DESC"

        if limit is not None:
            sql += " LIMIT :limit"
            params["limit"] = limit

        with self.engine.begin() as conn:
            rows = conn.execute(text(sql), params).fetchall()

        return [row[0] for row in rows]

    def fetch_latest_unseen(self) -> Optional[Tuple[int, str]]:
        """获取最新的未读数字"""
        with self.engine.begin() as conn:
            row = conn.execute(
                text(
                    """
                    SELECT id, value
                    FROM random_numbers
                    WHERE viewed = 0
                    ORDER BY id DESC
                    LIMIT 1
                    """
                )
            ).fetchone()

        if not row:
            return None
        return row[0], row[1]

    def mark_viewed(self, record_id: int) -> None:
        """标记某条记录为已读"""
        with self.engine.begin() as conn:
            conn.execute(
                text("UPDATE random_numbers SET viewed = 1 WHERE id = :record_id"),
                {"record_id": record_id},
            )

    def prune_excess(self, max_records: int) -> None:
        """仅保留最新的 max_records 条记录"""
        if max_records <= 0:
            return

        with self.engine.begin() as conn:
            extra_rows = conn.execute(
                text(
                    """
                    SELECT id
                    FROM random_numbers
                    ORDER BY id DESC
                    LIMIT :limit_value OFFSET :offset_value
                    """
                ),
                {"limit_value": 1000000, "offset_value": max_records},
            ).fetchall()

            ids_to_delete = [row[0] for row in extra_rows]
            if not ids_to_delete:
                return

            delete_stmt = (
                text("DELETE FROM random_numbers WHERE id IN :ids").bindparams(
                    bindparam("ids", expanding=True)
                )
            )
            conn.execute(delete_stmt, {"ids": ids_to_delete})
