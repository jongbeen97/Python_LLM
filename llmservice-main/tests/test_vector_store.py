import sys
import os
import unittest
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.vector_store import VectorStore


class TestVectorStore(unittest.TestCase):
    def setUp(self):
        self.test_dir = "./test_db"
        self.collection_name = "test_collection"
        self.store = VectorStore(
            collection_name=self.collection_name, persist_directory=self.test_dir
        )
        # 테스트 종료시 생성된 테스트 폴더 자동 삭제 처리

    def testDown(self):
        if os.path.exists(self.test_dir):
            # ignore_errors=True를 쓰면 프로세스가 사용 중이라도 에러로 멈추지 않습니다.
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_add_and_count(self):
        self.store.add_item(
            item_id="apple",
            embedding=[1.0, 0.0, 0.0],
            metadata={"type": "fruit", "name": "사과"},
        )
        count = self.store.get_collection_count()
        self.assertEqual(count, 1)

    # 유사도 검색
    def test_search(self):
        items = [
            {
                "id": "apple",
                "embedding": [1.0, 0.0, 0.0],
                "metadata": {"type": "fruit", "name": "사과"},
            },
            {
                "id": "computer",
                "embedding": [0.0, 0.0, 1.0],
                "metadata": {"type": "tech", "name": "컴퓨터"},
            },
        ]
        self.store.add_items(items)

        # 사과와 비슷한 백터로 검색 [0.9,0.1,0.0]
        results = self.store.search(query_embedding=[0.9, 0.1, 0.0], n_results=1)

        # 결과가 사과가 나오는지 확인
        self.assertEqual(results[0]["id"], "apple")
        print(f"유사도검색완료 (결과: {results[0]['metadata']['name']})")

        # 데이터 삭제

    def test_exist_and_delete(self):
        item_id = "apple"
        result = self.store.delete_item(item_id)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
