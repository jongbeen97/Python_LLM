# 백터 디비 서비스 - 크로마 디비 사용하여 백터 저장 및 검색
import chromadb
from typing import Optional, List, Dict, Any


class VectorStore:
    def __init__(self, collection_name: str, persist_directory: Optional[str] = None):
        self.collection_name = collection_name

        if persist_directory:
            self.client = chromadb.PersistentClient(
                path=persist_directory
            )  # 영구적으로 저장
        else:
            self.client = (
                chromadb.Client()
            )  # 프로그램 종료시까지만 유지 ( 프로젝트 메모리에 저장)
            # 컬렉션 생성
            # 두데이터의 유사도 계산 - 코사인 유사도 사용
        self.collection = self.client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"}
        )
        # DB에 단일 데이터 저장

    def add_item(
        self,
        item_id: str,  #  데이터의 PK (고유번호) ex)책의 ISBN
        embedding: List[float],  # (숫자로 변환된 리스트 ) ex) 책의 내용이 저장
        metadata: Dict[str, Any],
    ) -> None:  # 데이터의 부가 정보
        self.collection.add(ids=[item_id], embeddings=[embedding], metadatas=[metadata])
        # DB에 대량 데이터 저장

    def add_items(self, items: List[Dict[str, Any]]) -> None:  # 데이터의 부가 정보
        ids = [item["id"] for item in items]
        embeddings = [item["embedding"] for item in items]
        metadatas = [item["metadata"] for item in items]
        self.collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)

        # 유사한 아이템 검색 - 질문과 가장 비슷한 내용의 아이템 찾기

    def search(
        self,
        query_embedding: List[float],  # 사용자의 질문을 숫자로 변환한 벡터
        n_results: int = 5,  # 검색 결과로 몇개를 반환할지 설정
    ) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=n_results
        )
        print("변환전 results 결과 : \n", results)
        items = []
        # 검색된 결과를 사용하기 편한 리스트 - 딕셔너리 형태로 재구성
        # distance : 질문과 얼마나 거리가 먼지 나타냄 -> 0에 가까울 수록 비슷한 내용(유사도 ↑)
        for i in range(len(results["ids"][0])):
            item = {
                "id": results["ids"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            }
            items.append(item)
        return items

    # 현재 저장된 아이템의 갯수를 알려주는 것
    def get_collection_count(self) -> int:
        return self.collection.count()

    # 이 아이템이 저장되어 있는지 확인
    def exist(self, item_id: str) -> bool:
        return self.collection.get(ids=[item_id]) is not None

    # 아이템 추가하기 (중복확인을 한 후 , 추가를 해야 한다 , 중복이 되지 않도록 = Update & Insert)
    def upsert_item(
        self,
        item_id: str,  #  데이터의 PK (고유번호) ex)
        embedding: List[float],  # (숫자로 변환된 리스트 ) ex)
        metadata: Dict[str, Any],
    ) -> bool:  # 데이터의 부가 정보
        if self.exist(item_id):
            return False
        self.collection.add_item(
            ids=[item_id], embeddings=[embedding], metadatas=[metadata]
        )
        return True

    # 아이템 삭제
    def delete_item(self, item_id: str) -> bool:
        if not self.exist(item_id):
            return False
        self.collection.delete(ids=[item_id])
        return True

    # 모든 아이템 전체 삭제
    def delete_collection(self) -> None:
        self.client.delete_collection(name=self.collection_name)
