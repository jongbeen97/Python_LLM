import pytest
import sys
import os
from dotenv import load_dotenv

# 테스트 시작 전 .env 파일로드
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.mysql_connection import MySQLConnection
from src.models.clothing import Clothing, ClothingCategory, Color, Season, Style
from src.database.clothing_repository import ClothingRepository


class TestSampleData:

    @classmethod
    def setup_class(cls):
        cls.repo = ClothingRepository()

    def test_database_init(self):
        print("데이터베이스 초기화 시작 ")
        try:
            MySQLConnection.init_database()
            print("데이터베이스 초기화 성공")
        except Exception as e:
            pytest.fail(f"데이터베이스 초기화 실패 : {e}")

    # 샘플 상품 데이터 여부 확인
    def test_sample_products_count(self):
        # 전체 데이터 갯수가  32개인지 확인
        count = self.repo.count()
        print("전체 데이터 갯수: ", count)
        assert count >= 32

    # 모든 데이터를 객체로 변환
    def test_get_all_products(self):
        products = self.repo.get_all()
        assert len(products) > 0
        # Clothing 객체 여부 판단
        assert hasattr(products[0], "name")
        print(f"첫번째 상품 확인: {products[0].name} {products[0].category.value}")

    # 카테고리별 조회 확인
    def test_get_products_by_category(self):
        products = self.repo.get_by_category(ClothingCategory.TOP)
        print(f"상의 갯수 : {len(products)}")


if __name__ == "__main__":
    # 수동으로 테스트파일 실행, 자동 실행 두 경우 모두 테스트 동작
    pytest.main([__file__, "-s"])
