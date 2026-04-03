# 텍스트 -> 임베딩 변환 함수
# 임베딩 : 벡터는 텍스트를 숫자리스트로 변환한다.
# 인공지능이 단어의 의미를 숫자 리스트로 바꿔서 이해하는 과정
from google import genai
from typing import List  # 기본 타입이 아닌 경우는 전부 import해야 함.


class EmbeddingService:

    def __init__(self, api_key: str, model: str = "models/gemini-embedding-001"):
        self.api_key = api_key
        self.model = model
        self.client = genai.Client(
            api_key=self.api_key
        )  # 클라이언트라는 키에다 , gemini에서 클라이언트가 있는데 , 재미나이 클라이언트 API에 self.api._key를 집어넣어준다. 재미나이에게 요청을 하도록 처리

    # 단일 텍스트를 임베딩 벡터로 변환
    # "사과" -> [0.12,0.11,0.22] 이렇게 변환한다는 것, 리스트 형태인데 그 리스트 안에는 float 형태 들어감
    def embed_text(self, text: str) -> List[float]:
        # API를 호출하여 임베딩 결과 생성
        response = self.client.models.embed_content(model=self.model, contents=text)
        # response 에서 숫자 리스트만 뽑아서 반환
        # response.embeddings[0] : 첫번째 입력 테스트에 대한 결과
        return list(response.embeddings[0].values)

    # 여러개의 텍스트를 한꺼번에 임베딩 벡터로 변환
    # ["사과","포도"] -> [[0.12,0.11,0.22],...] 이중리스트로 나오게
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        embeddings = []

        for text in texts:
            # 각 단어를 하나씩 꺼내서 embed_text()를 이용하여 벡터로 변환 후 리스트에 추가
            embeddings.append(self.embed_text(text))
        return embeddings
