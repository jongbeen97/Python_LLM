"""
해야 하는 것
1. 실시간 날씨 확인
2. 질문과 날씨에 어울리는 옷 검색
3. 검색한 정보(Vector DB에서)를 바탕으로 LLM 답변 생성
"""

from typing import Optional, List, Dict

from src.models.clothing import ClothingCategory, Season, Style, Color
from src.database.clothing_repository import ClothingRepository
from src.vector_store import VectorStore
from src.embedding_service import EmbeddingService
from src.models.clothing import Clothing
from src.database.mysql_connection import MySQLConnection
from src.models.clothing import ClothingCategory, Season
from src.clothing_service import ClothingService
from src.weather_service import WeatherService, WeatherInfo
from src.llm_service import LLMService


# 역할 부여를 해주어야 한다 ( 기본 프롬프트 만들기 )
OUTFIT_SYSTEM_PROMPT = """당신은 날씨 기반 패션 코디네이터 입니다.
사용자의 질문에 맞는 의상을 사용자의 옷장에 있는 옷을 기반으로,
날씨와 상황(TPO)에 맞는 최적의 코디를 추천해주세요. 
## 추천 원칙
1. 날씨 고려 : 기온에 맞는 보온성, 비나 눈이 오면 방수 아이템
2. TPO 고려 : 데이트/출근/운동/면접 등 상황에 맞는 스타일
3. 색상 조화 : 어울리는 색상 조합(유사색)
4. 스타일 통일 : 캐주얼/스포티 등 일관된 무드 

## 답변 형식 
1. 오늘의 코드 추천 : 상의 + 하의 + 아우터(필요시) + 신발 + 액세서리,가방(필요시)
2. 각 아이템을 선택한 이유
3. 전체 코디의 포인트 설명 
친근하고 자연스러운 톤으로 답변해주세요. 반드시 옷장에 있는 옷 이름을 정확히 사용하세요. 
"""

# self : 클래스 내부에 메서드 선언을 할 경우 반드시 Self라는 변수가 들어가야 함.


# 클래스 생성
class OutfitRecommendationService:
    # 초기화 , 생성자 (constructor), 객체 만들어질때 자동으로 실행되는 초기 함수
    def __init__(
        self,  # 나 자신을 가져오는 것
        gemini_api_key: str,  # 외부에서 Gemini_KEY를 가져옴
        collection_name: str = "clothes",  # VectorDB에서 옷을 가져온다.
        persist_directory: str = "./chroma_clothes",  # 백터 에 저장되는 DB 크로마 DB 가져오기
    ):
        # 옷 데이터 관리 및 DB 초기화 담당 해주는 기능 ( clothing_service ) 객체 생성
        #
        self.clothing_service = ClothingService(  # clothing_service 객체를 불러옴
            api_key=gemini_api_key,  # AI 기능 사용위해 인증키 전달
            collection_name=collection_name,  # `clothes`라는 이름의 데이터 보관함을 지정
            persist_directory=persist_directory,  # 데이터가 저장될
        )
        # 기상청 API를 통한 실시간 날씨 조회 담당, 실시간 날씨를 확인을 해야 하니 가져옴
        self.weather_service = WeatherService()
        # text를 숫자로 변환하는 AI 모델 담당하는 임베딩 기능 가져오기 ,  실시간 날씨를 가져오면 , 이를 저장하기 위해서 숫자로 임베딩 해야 함
        self.embedding_service = EmbeddingService(api_key=gemini_api_key)
        # 벡터 DB 검색을 담당하는 서비스 가져와야 함 ( 벡터 서비스 )
        self.vector_store = VectorStore(
            collection_name=collection_name, persist_directory=persist_directory
        )
        # 최종 답변을 생성하는 생성형 AI 담당
        self.llm_service = LLMService(
            api_key=gemini_api_key, system_prompt=OUTFIT_SYSTEM_PROMPT
        )

        # 사용자 질문에 맞춰서 날씨를 고려한 코디를 생성해주는 기능
        # 날씨 조회 -> 날씨에 맞춘 최적화된 검색어들을 생성 (LLM이 뽑아내야 함)

    def get_weather(self, city: str = "서울") -> Optional[WeatherInfo]:
        return self.weather_service.get_weather(city)

        # LLM이 백터에서 검색을 함. -> 프롬프트 빌드를 해야 함 -> LLM 이 답변을 할수 있는 것이다.

    def recommend_outfit(self, user_query: str) -> str:
        # 1. 날씨조회를 해야 함
        # (default : 매개변수가 없으므로 기본 값이 서울 날씨를 조회하게 됨)
        weather = self.weather_service.get_weather()
        weather_desc = (
            weather.to_description() if weather else "날씨 정보를 가져오지 못했습니다"
        )  # 웨더가 있다면 앞의 문장 실행, 없으면 뒤의 문자 출력

        # 날씨 데이터를 검색용 최적의 텍스트로 변환
        # 예시 ) 현재 25도 맑음 상태 -> 여름 날씨, 시원한 옷 , 반팔 이런 것을 추천해야 함.
        # 즉 , 검색에 도움되는 키워드를 생성해야 함.
        if weather:
            season = weather.get_season()
            weather_query = f"{season} 날씨, {weather.temperature}도,{'비' if weather.rain else '눈' if weather.snow else ''}"
        else:
            weather_query = ""
            # 사용자의 실제 질문과 날씨 정보를 합쳐서 검색 의도를 파악해야 함
            # ex)오늘 뭐 입는게 좋아 ? + 여름날씨, 시원한 옷, 반팔
        search_query = (
            f"{user_query}, {weather_query}".strip()
        )  # strip() : 문자열에서 원하는 문자열, 혹은 공백을 모두 제거할 수 있는 기능을 가지고 있음.
        query_embedding = self.embedding_service.embed_text(search_query)
        # 2. 백터 에서 질문과 가장 의미가 가까운 옷 (유사도가 높은 옷) 검색 해보기
        search_results = self.vector_store.search(query_embedding, n_results=7)
        # search_results 에 결과가 없다. : 현재 날씨에 맞는 옷이 없다..
        if not search_results:
            return "옷장에 등록된 옷이 없습니다. 먼저 옷을 등록해주세요."
        # 찾아온 옷들을 카테고리 별로 정리
        clothes_by_category = self._categorize_clothes(search_results)

        # LLM 에게 전달할 최종 프롬프트 생성
        prompt = self._build_recommendation_prompt(
            user_query=user_query,
            weather_desc=weather_desc,
            clothes_by_category=clothes_by_category,
            weather=weather,
        )

        # 최종 답변을 생성해주는 기능
        return self.llm_service.generate(prompt)

        # 검색 결과로 나온 많은 옷들을 상의, 하의,아우터 등 카테고리 별로 분류
        # AI가 코디를 조합하기 편하게 정리하는 함수

    def _categorize_clothes(self, search_results: List[Dict]) -> Dict[str, List[Dict]]:
        categorize = {
            "아우터": [],
            "상의": [],
            "하의": [],
            "원피스": [],
            "신발": [],
            "액세서리": [],
        }
        for result in search_results:
            metadata = result["metadata"]
            category = metadata["category"]  # metadata.get("key") 도 가능
            if category in categorize:
                categorize[category].append(metadata)
        return categorize

    def _build_recommendation_prompt(
        self,
        user_query: str,
        weather_desc: str,
        clothes_by_category: Dict[str, List[Dict]],
        weather: Optional[WeatherInfo] = None,
    ) -> str:
        prompt_parts = []

        # 날씨 정보 추가
        prompt_parts.append("##오늘의 날씨")
        prompt_parts.append(weather_desc)

        # 날씨에 따른 특수 조언 추가
        if weather:
            season = weather.get_season()
            prompt_parts.append(f"추천 계절감: {season}")
            if weather.rain:
                prompt_parts.append("비가오고 있습니다 - 방수 아우터 고려")
            if weather.snow:
                prompt_parts.append("눈이오고 있습니다 - 미끄럽지 않은 신발 고려")
        # 사용자의 원래 요청 사항
        prompt_parts.append("\n##사용자의 요청")
        prompt_parts.append(user_query)

        # 검색을 통한 찾은 사용자의 옷장 데이터
        prompt_parts.append("\n##사용자의 옷장")
        for category, clothes in clothes_by_category.items():
            if clothes:
                prompt_parts.append(f"##{category}")
                for cloth in clothes:
                    warmth = cloth.get("warmth_level", 3)
                    warmth_desc = (
                        "따듯" if warmth >= 4 else "보통" if warmth >= 2 else "시원"
                    )
                    prompt_parts.append(
                        f"-{cloth.get('name','이름없음')} ,"
                        f"(색상 : {cloth.get('color',' ')}),"
                        f"스타일: {cloth.get('style',' ')},"
                        f"보온성: {warmth_desc})"
                    )
        prompt_parts.append("##요청사항")
        prompt_parts.append(
            "위 옷장의 옷들 중에서 오늘 날씨와 사용자 요청에맞는 코디를 추천해주세요."
        )
        prompt_parts.append(
            "반드시 상의 +하의+신발 조합을 포함하고 날씨에 따라 아우터도 추천해주세요"
        )

        return "\n".join(prompt_parts)
