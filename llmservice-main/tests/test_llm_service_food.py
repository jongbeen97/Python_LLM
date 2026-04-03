import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_service import LLMService;

class test_llm_service:
    def __init__(self, api_key: str):
        self.service = LLMService(api_key=api_key)

    def test_generate(self):
        prompt = "오늘의 비만 남성의 다이어트 식단을 추천해줘"
        response = self.service.generate(prompt)
        print(f"테스트 응답: {response}")
        assert response is not None

    def test_recommendation(self):
        query = "내가 가지고 있는 식품들을 통해서  다이어트를 할수 있도록 식단을 짜줘"
        context_items = [
            {"상품명": "하림 닭가슴살", "카테고리": "다이어트 식품", "특징": "다이어터들이 많이 먹는 식품"},
            {"상품명": "셀러드", "카테고리": "채소", "특징": "기본적인 다이어트 음식"},
            {"상품명": "단백질쉐이크", "카테고리": "다이어트 식품", "특징": "단백질 보충제"},
            {"상품명": "잡곡밥", "카테고리": "밥", "특징": "탄수화물 이지만 잡곡이 들어간 밥"},            
            {"상품명": "두부", "카테고리": "단백질,콩", "특징": "단백질이 있는 식품중 하나"},            
            {"상품명": "통밀빵", "카테고리": "빵", "특징": "탄수화물이지만 잡곡과 통밀로 만들어진 빵"}
        ]
        response = self.service.generate_recommendation(query, context_items)
        print(f"추천 테스트 응답: {response}")
        return response
    
if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    test = test_llm_service(api_key)
    test.test_generate()
    test.test_recommendation()
    

