# RAG 파이프 라인 : 질의(쿼리를 날림) -> 검색 -> 생성 통합
# 질의 -> 숫자 벼환( 임베딩)
# 벡터 디비에서 유사한 임베딩 정보를 찾아서 LLM + 백터 DB 통합 후 사용자에게 답변 전달

from src.llm_service import LLMService
from src.embedding_service import EmbeddingService
from src.vector_store import VectorStore


class RAGPipeline:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        llm_service: LLMService,
        vector_store: VectorStore,
    ):
        self.embedding_service = embedding_service
        self.llm_service = llm_service
        self.vector_store = vector_store

    # 사용자 질의에 대한 맞춤형 답변 생성 서비스
    def query(self, user_query: str, n_results: int = 5) -> str:
        # 1단계. 사용자의 질문을 백터(의미좌표)로 변환
        query_embedding = self.embedding_service.embed_text(user_query)
        # 2단계. 1단계에서 도출한 결과와 유사한 아이템을 벡터 DB에서 찾기 \
        search_results = self.vector_store.search(query_embedding, n_results)
        # 3단계. 문맥 추출 (예 : 시원한 상의 ) - 메타데이터만 모아서 정리
        context_items = [result["metadata"] for result in search_results]
        # 4단계 ; 생성단계 -> 사용자의 질문 + DB에서 찾은 관련지식 -> LLM  전달
        response = self.llm_service.generate_recommendation(user_query, context_items)
        return response
