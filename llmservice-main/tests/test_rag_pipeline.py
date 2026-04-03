import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.vector_store import VectorStore
from src.embedding_service import EmbeddingService
from src.llm_service import LLMService
from src.rag_pipeline import RAGPipeline


# 현업 스타일 테스트 진행
# 로직이 정상적으로 동작하는지 여부 확인
# 장점 : 비용과 시간 절약
# 단점 : 실제 서비스의 답변확인이 안됨
class TextRagPipeline:
    @pytest.fixture()
    def mock_pipeline(self):
        mock_embedding = Mock(spec=EmbeddingService)
        mock_llm = Mock(spec=LLMService)
        mock_vector_store = Mock(spec=VectorStore)

        # 가짜 서비스가 출력할 답변을 설정 (가짜 부품 세팅 )
        mock_embedding.embed_text.return_value = [0.1, 0.2, 0.3]
        mock_vector_store.search.return_value = [
            {
                "id": "c1",
                "metadata": {"name": "옷1", "description": "여름용 시원한 셔츠"},
                "distance": 0.05,
            }
        ]
        mock_llm.generate_recommendation.return_value = "옷1을 추천합니다"

        # 가짜 부품들 연결하는 파이프라인을 생성
        pipeline = RAGPipeline(
            embedding_service=mock_embedding,
            llm_service=mock_llm,
            vector_store=mock_vector_store,
        )
        return pipeline, mock_embedding, mock_llm, mock_vector_store

    # 테스트 진행 함수
    def test_query_integration(self, mock_pipeline):
        pipeline, mock_embedding, mock_llm, mock_vector_store = mock_pipeline
        user_query = "여름 날씨에 입기 좋은 옷을 추천해줘"

        # 사용자가 질문을 전달했을때
        result = pipeline.query(user_query)
        # 사용자의 질문이 숫자로 변환되었는지 확인
        mock_embedding.embed_text.assert_called_once_with(user_query)
        # 변환된 숫자로 DB 검색이 실행되었는지 확인
        mock_vector_store.search.assert_called_once_with([0.1, 0.2, 0.3], 5)
        # LLM 이 검색결과를 바탕으로 답변을 잘 만들었는지 확인
        mock_llm.generate_recommendation.assert_called_once()

        # 최종 결과 확인
        assert result == "옷1을 추천합니다"  # 파이프라인 잘 연결되었을때 나오는 것
        print(f"파이프라인 테스트 통과 (결과:{result})")


if __name__ == "__main__":
    pytest.main()
