"""옷 데이터 Repository"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Optional
from datetime import datetime

from .mysql_connection import MySQLConnection
from src.models.clothing import Clothing, ClothingCategory, Color, Season, Style


class ClothingRepository:
    """옷 데이터 CRUD Repository"""

    @staticmethod
    def _row_to_clothing(row: tuple) -> Clothing:
        """DB 행을 Clothing 객체로 변환"""
        return Clothing(
            id=row[0],
            name=row[1],
            category=ClothingCategory(row[2]),
            color=Color(row[3]),
            season=Season(row[4]),
            style=Style(row[5]),
            description=row[6],
            brand=row[7],
            image_url=row[8],
            warmth_level=row[9],
            created_at=row[10],
        )

    def add(self, clothing: Clothing) -> int:
        """옷 추가"""
        conn = MySQLConnection.get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO clothes (name, category, color, season, style, description, brand, image_url, warmth_level)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (
                clothing.name,
                clothing.category.value,
                clothing.color.value,
                clothing.season.value,
                clothing.style.value,
                clothing.description,
                clothing.brand,
                clothing.image_url,
                clothing.warmth_level,
            ),
        )

        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return new_id

    def get_by_id(self, clothing_id: int) -> Optional[Clothing]:
        """ID로 옷 조회"""
        conn = MySQLConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, category, color, season, style, description, brand, image_url, warmth_level, created_at FROM clothes WHERE id = %s",
            (clothing_id,),
        )
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return self._row_to_clothing(row)
        return None

    def get_all(self) -> List[Clothing]:
        """모든 옷 조회"""
        conn = MySQLConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, category, color, season, style, description, brand, image_url, warmth_level, created_at FROM clothes ORDER BY created_at DESC"
        )
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [self._row_to_clothing(row) for row in rows]

    def get_by_season(self, season: Season) -> List[Clothing]:
        """계절별 옷 조회"""
        conn = MySQLConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, category, color, season, style, description, brand, image_url, warmth_level, created_at FROM clothes WHERE season = %s OR season = '사계절'",
            (season.value,),
        )
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [self._row_to_clothing(row) for row in rows]

    def get_by_category(self, category: ClothingCategory) -> List[Clothing]:
        """카테고리별 옷 조회"""
        conn = MySQLConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, category, color, season, style, description, brand, image_url, warmth_level, created_at FROM clothes WHERE category = %s",
            (category.value,),
        )
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [self._row_to_clothing(row) for row in rows]

    def get_by_warmth_range(self, min_warmth: int, max_warmth: int) -> List[Clothing]:
        """보온성 범위로 옷 조회"""
        conn = MySQLConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, category, color, season, style, description, brand, image_url, warmth_level, created_at FROM clothes WHERE warmth_level BETWEEN %s AND %s",
            (min_warmth, max_warmth),
        )
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [self._row_to_clothing(row) for row in rows]

    def delete(self, clothing_id: int) -> bool:
        """옷 삭제"""
        conn = MySQLConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM clothes WHERE id = %s", (clothing_id,))
        affected = cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()

        return affected > 0

    def count(self) -> int:
        """총 옷 개수"""
        conn = MySQLConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM clothes")
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return count
