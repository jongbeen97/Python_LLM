import sys
import os
# 경로 설정 : src 폴더의 embedding_service파일 사용을 위해서 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.embedding_service import EmbeddingService;

class test_embedding_service:
   def __init__(self,api_key:str):
      self.service = EmbeddingService(api_key=api_key)

   def test_embed_text(self):
      print("\n===[단일 문장 임베딩 테스트]===")
      text = "오늘 날씨에 어울리는 옷을 추천해줘"
      
      vector = self.service.embed_text(text)

      print(f"입력문장: {text}")
      print(f"임베딩 벡터: {vector}")
      print(f"벡터 크기(차원): {len(vector)}")
      print(f"벡터 값 확인 : {vector[:5]}...")

      #검증하기 : assert (너 맞아? 테스트에는 필수적으로 사용)
      #결과 값이 숫자 리스트 이면서 비어있지 않은지 확인 
      assert vector is not None and len(vector) > 0
      return vector
   
if __name__ == "__main__":
  api_key = "--"
  test = test_embedding_service(api_key)
  test.test_embed_text()
