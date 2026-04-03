import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_service import LLMService;

class test_llm_service:
    def __init__(self, api_key: str):
        self.service = LLMService(api_key=api_key)

    def test_generate(self):
        prompt = "오늘 날씨에 어울리는 옷을 추천해줘."
        response = self.service.generate(prompt)
        print(f"테스트 응답: {response}")
        assert response is not None

    def test_recommendation(self):
        query = "운동용으로 입을 만한 옷이 있을까? 내가 가지고 있는 옷이 없다면 '브랜드:가격:상품명:특징'형식으로 추천해줘"
        context_items = [
            {"상품명": "블랙 맞춤 수트", "카테고리": "정장", "특징": "깔끔하고 세련된 핏"},
            {"상품명": "화이트 셔츠", "카테고리": "상의", "특징": "기본적인 셔츠"},
            {"상품명":"유니클로 민소매 러닝 티셔츠","카테고리":"운동상의","특징":"여름 러닝할때 효과적임"}
        ]
        response = self.service.generate_recommendation(query, context_items)
        print(f"추천 테스트 응답: {response}")
        return response

if __name__ == "__main__":
    API_KEY ="AIzaSyClhxvEu6n0HCKowjTykCpZI0obWR6ynNM"
    tester = test_llm_service(API_KEY)
    tester.test_generate()
    tester.test_recommendation()