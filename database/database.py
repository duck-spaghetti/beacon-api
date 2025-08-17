import sqlite3
from typing import Any, Dict, List, Optional, Tuple

class Database:
    def __init__(self, db_path: str = "database/poi.db"):
        self.db_path = db_path

    def execute_query(self, query: str, params: Tuple[Any, ...] = ()) -> List[sqlite3.Row]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_non_query(self, query: str, params: Tuple[Any, ...] = ()) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def insert_poi(self, data: Dict[str, Any]) -> int:
        query = (
            """
            INSERT INTO poi (
                latitude, longitude, address, city, phone, transport,
                is_active, name, info_it, info_en, info_ar, time_table, type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        )
        params = (
            data["latitude"],
            data["longitude"],
            data.get("address"),
            data.get("city"),
            data.get("phone"),
            data.get("transport"),
            data.get("is_active", True),
            data.get("name"),
            data.get("info_it"),
            data.get("info_en"),
            data.get("info_ar"),
            data.get("time_table"),
            data.get("type"),
        )
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid

    def update_poi(self, poi_id: int, data: Dict[str, Any]) -> None:
        if not data:
            return
        fields = ", ".join(f"{k} = ?" for k in data.keys())
        params = list(data.values()) + [poi_id]
        query = f"UPDATE poi SET {fields} WHERE id = ?"
        self.execute_non_query(query, tuple(params))

    def delete_poi(self, poi_id: int) -> None:
        self.execute_non_query("DELETE FROM poi WHERE id = ?", (poi_id,))

    def get_poi_by_id(self, poi_id: int) -> Optional[Dict[str, Any]]:
        rows = self.execute_query("SELECT * FROM poi WHERE id = ?", (poi_id,))
        return dict(rows[0]) if rows else None

