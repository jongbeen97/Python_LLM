# MySQL(원본데이터)과 VectorDB(AI 검색용 데이터)의 연결을 해주는 서비스 클래스
from typing import Optional, List

from src.database.clothing_repository import ClothingRepository
from src.vector_store import VectorStore
from src.embedding_service import EmbeddingService
from src.models.clothing import Clothing
from src.database.mysql_connection import MySQLConnection
from src.models.clothing import ClothingCategory, Season


class ClothingService:
    def __init__(
        self,
        api_key: str,
        collection_name: str = "clothes",
        persist_directory: str = "./chroma_clothes",
    ):
        # MySQL 조작을 담당하는 저장소 (Repository)
        self.repository = ClothingRepository()
        # 임베딩 서비스(숫자로 변환을 해야지 LLM이 기억을 하기 때문에)
        # 텍스트를 숫자로 변환
        self.embedding_service = EmbeddingService(api_key)
        # 벡터 디비 : 크로마 생성
        # 검색용 벡터 데이터를 저장하는 chromaDB
        self.vector_store = VectorStore(collection_name, persist_directory)

    # 새옷을 등록 ( MySQL 에도 저장이 되어야 하고 , 검색도 해야 하니 vectorDB에도 저장이 되어야 함)
    def add_clothing(self, clothing: Clothing) -> int:
        # MySQL에 데이터 저장후 자동생성된 ID 받아오기
        new_id = self.repository.add(clothing)
        clothing.id = new_id  # 여기는 MYSQL에 저장

        # AI 검색 , 옷정보 검색에 최적화된 정보를 주어야 함.
        # 벡터 DB가 이해할 수 있는 최적의 텍스트로 변한하는 것
        text = (
            clothing.to_text()
        )  # 사용자가 입력한 옷을 백터 디비가 알아듣도록 텍스트 생성
        embedding = self.embedding_service.embed_text(
            text
        )  # 벡터 변환 : 텍스트를 숫자로 변환
        # 벡터 저장하는 부분
        self.vector_store.add_item(  # SQL과 벡터가 연동이 되어야 한다.
            item_id=f"cloth_{new_id}",  # MySQL ID와 매칭되도록 규칙 설정
            embedding=embedding,
            metadata=clothing.to_dict(),
        )
        return new_id

    # 옷을 삭제하는 함수 MySQL과 백터 두군데에 모두 삭제 되어야 한다.
    def delete_clothing(self, clothing_id: int) -> bool:
        # MySQL 에서 옷을 삭제
        result = self.repository.delete(clothing_id)
        # 백터 에서 옷 삭제
        if result:
            try:
                self.vector_store.delete_item(f"cloth_{clothing_id}")
            except Exception:
                pass  # 그냥 넘어가 ~~ 라는 의미이다.
            return result

    ## MySQL에만 있고 백터 DB에 없는 데이터 찾아 복사
    # 초기 세팅 및 데이터 유실시 필수로 필요한 기능입니다
    def sync_to_vector_db(self) -> dict:
        # MySQL에 저장된 모든 옷 정보를 가져오기
        clothes = self.repository.get_all()
        synced = 0

        for clothing in clothes:
            item_id = f"cloth_{clothing.id}"
            # 백터에 저장된 항목인지 체크 (중복 추가를 방지를 하기 위해서)
            # if self.vector_store.exist(item_id):  # 이게 백터에 존재해 ?
            #     continue
            # 없는 옷만 임베딩 작업 후 벡터에 추가하는 것
            text = clothing.to_text()
            embedding = self.embedding_service.embed_text(text)
            self.vector_store.add_item(
                item_id=item_id,
                embedding=embedding,
                metadata=clothing.to_dict(),
            )
            synced += 1
        return {
            "total": len(clothes),
            "synced": synced,
        }

    @staticmethod
    def init_database():
        MySQLConnection.init_database()

    def get_all_clothes(self) -> list[Clothing]:
        return self.repository.get_all()

    def get_by_id(self, clothing_id: int) -> Optional[Clothing]:
        return self.repository.get_by_id(clothing_id)

    def get_by_season(self, season: Season) -> List[Clothing]:
        return self.repository.get_by_season(season)

    def get_by_category(self, category: ClothingCategory) -> List[Clothing]:
        return self.repository.get_by_category(category)

    def get_by_warmth_range(self, min_warmth: int, max_warmth: int) -> List[Clothing]:
        return self.repository.get_by_warmth_range(min_warmth, max_warmth)

    def count(self) -> int:
        return self.repository.count()
