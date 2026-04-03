# # [날씨 기반 코디 추천 시스템]
# import os

# # 분산되어 있는 각 서비스를 하나로 묶어서 프로그램 실행
# from dotenv import load_dotenv

# # 보안을 위해 API 키와 DB 정보를 환경변수에서 읽어오도록
# # 시작전 env 파일 로드
# load_dotenv(os.path.join(os.path.dirname(__file__), ".env.dev"))
# # 개발도구랑 환경 변수 파일 !!
# # 나머지들 다 연결시켜 주어야 한다 ! ( 서비스나 이런 것들 !! )
# [날씨 기반 코디 추천 시스템]
# 분산되어 있는 각 서비스를 하나로 묶어 프로그램 실행
import os
from dotenv import load_dotenv

load_dotenv()

from src.outfit_recommendation_service import OutfitRecommendationService
from src.clothing_service import ClothingService

# 보안을 위해 API키와 DB정보를 환경 변수에서 읽어오도록
# 시작전 .env 파일 로드
# main.py 상단 수정 제안
import os
from dotenv import load_dotenv

# 기존 코드보다 더 확실하게 현재 경로를 잡는 방법
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, ".env.dev")

if os.path.exists(env_path):
    load_dotenv(env_path)
    print(f">> 환경 설정 파일 로드 성공: {env_path}")
else:
    print(f"경고: {env_path} 파일을 찾을 수 없습니다!")


# 샘플 옷 데이터
SAMPLE_CLOTHES = [
    # 아우터 (6개)
    (
        "검정 롱패딩",
        "아우터",
        "블랙",
        "겨울",
        "캐주얼",
        "무릎까지 오는 따뜻한 롱패딩",
        "노스페이스",
        5,
    ),
    (
        "베이지 트렌치코트",
        "아우터",
        "베이지",
        "가을",
        "미니멀",
        "클래식 트렌치코트",
        "버버리",
        3,
    ),
    (
        "네이비 블레이저",
        "아우터",
        "네이비",
        "사계절",
        "포멀",
        "비즈니스 자켓",
        "지오다노",
        2,
    ),
    (
        "카키 야상",
        "아우터",
        "그린",
        "봄",
        "캐주얼",
        "밀리터리 야상 점퍼",
        "유니클로",
        3,
    ),
    (
        "그레이 후드집업",
        "아우터",
        "그레이",
        "봄",
        "스포티",
        "운동용 후드 집업",
        "나이키",
        2,
    ),
    (
        "브라운 가죽자켓",
        "아우터",
        "브라운",
        "가을",
        "스트릿",
        "빈티지 라이더 자켓",
        "올세인츠",
        3,
    ),
    # 상의 (8개)
    (
        "흰색 기본 티셔츠",
        "상의",
        "화이트",
        "여름",
        "캐주얼",
        "깔끔한 면 티셔츠",
        "무인양품",
        1,
    ),
    (
        "네이비 옥스포드 셔츠",
        "상의",
        "네이비",
        "사계절",
        "포멀",
        "비즈니스 캐주얼 셔츠",
        "랄프로렌",
        2,
    ),
    ("스트라이프 셔츠", "상의", "블루", "봄", "캐주얼", "파란 줄무늬 셔츠", "자라", 2),
    (
        "그레이 캐시미어 니트",
        "상의",
        "그레이",
        "겨울",
        "미니멀",
        "캐시미어 스웨터",
        "유니클로",
        4,
    ),
    ("검정 터틀넥", "상의", "블랙", "겨울", "미니멀", "따뜻한 터틀넥", "COS", 4),
    (
        "베이지 맨투맨",
        "상의",
        "베이지",
        "가을",
        "캐주얼",
        "오버핏 맨투맨",
        "아디다스",
        3,
    ),
    ("핑크 블라우스", "상의", "핑크", "봄", "포멀", "실크 블라우스", "마시모두띠", 2),
    ("화이트 크롭탑", "상의", "화이트", "여름", "스트릿", "시원한 크롭 티", "H&M", 1),
    # 하의 (6개)
    ("검정 슬랙스", "하의", "블랙", "사계절", "포멀", "정장 바지", "지오다노", 3),
    (
        "인디고 청바지",
        "하의",
        "블루",
        "사계절",
        "캐주얼",
        "스트레이트핏 데님",
        "리바이스",
        3,
    ),
    ("베이지 치노팬츠", "하의", "베이지", "봄", "캐주얼", "면 치노 팬츠", "갭", 2),
    (
        "화이트 와이드팬츠",
        "하의",
        "화이트",
        "여름",
        "미니멀",
        "린넨 와이드 팬츠",
        "자라",
        1,
    ),
    (
        "그레이 조거팬츠",
        "하의",
        "그레이",
        "사계절",
        "스포티",
        "운동용 조거",
        "나이키",
        3,
    ),
    ("네이비 반바지", "하의", "네이비", "여름", "캐주얼", "여름용 반바지", "폴로", 1),
    # 신발 (5개)
    (
        "흰색 운동화",
        "신발",
        "화이트",
        "사계절",
        "캐주얼",
        "캔버스 스니커즈",
        "컨버스",
        2,
    ),
    ("검정 로퍼", "신발", "블랙", "사계절", "포멀", "가죽 로퍼", "콜한", 2),
    (
        "브라운 첼시부츠",
        "신발",
        "브라운",
        "겨울",
        "캐주얼",
        "가죽 앵클부츠",
        "닥터마틴",
        4,
    ),
    ("베이지 슬립온", "신발", "베이지", "여름", "미니멀", "캔버스 슬립온", "반스", 1),
    ("네이비 러닝화", "신발", "네이비", "사계절", "스포티", "러닝화", "뉴발란스", 2),
    # 액세서리 (4개)
    ("블랙 가죽벨트", "액세서리", "블랙", "사계절", "포멀", "소가죽 벨트", "몽블랑", 2),
    ("베이지 버킷햇", "액세서리", "베이지", "여름", "캐주얼", "면 버킷햇", "캉골", 1),
    ("그레이 머플러", "액세서리", "그레이", "겨울", "미니멀", "울 머플러", "아크네", 5),
    (
        "브라운 토트백",
        "액세서리",
        "브라운",
        "사계절",
        "캐주얼",
        "가죽 토트백",
        "코치",
        2,
    ),
]


def insert_sample_clothes():
    """샘플 옷 데이터를 MySQL에 삽입"""
    import mysql.connector

    conn = mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        port=int(os.environ.get("MYSQL_PORT", "3306")),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", "0000"),
        database=os.environ.get("MYSQL_DATABASE", "clothing_db"),
        charset="utf8mb4",
    )
    cursor = conn.cursor()
    sql = """
        INSERT INTO clothes (name, category, color, season, style, description, brand, warmth_level)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(sql, SAMPLE_CLOTHES)
    conn.commit()
    cursor.close()
    conn.close()
    return len(SAMPLE_CLOTHES)


def run_demo():
    """코디 추천 데모 실행"""
    gemini_key = os.environ.get("GEMINI_API_KEY")
    kma_key = os.environ.get("KMA_API_KEY")

    if not gemini_key:
        print("오류: GEMINI_API_KEY 환경변수를 설정해주세요.")
        return

    print("=" * 50)
    print("[날씨 기반 코디 추천 시스템 v1.1]")
    print("=" * 50)

    # 1. DB 초기화 (MySQL)
    try:
        print(">> 데이터베이스 연결 중...")
        ClothingService.init_database()
    except Exception as e:
        print(f"DB 연결 실패: {e}")
        return

    # 2. 서비스 초기화
    try:
        service = OutfitRecommendationService(gemini_api_key=gemini_key)
    except Exception as e:
        print(f"서비스 초기화 실패: {e}")
        return

    # 3. [중요] 벡터 DB 강제 초기화 (최초 1회 데이터 유실 방지용)
    # 검색 결과가 안 나올 때 이 코드를 활성화해서 돌리면 해결됩니다.
    print(">> 벡터DB 강제 초기화 및 재색인 시작...")
    try:
        # 기존 컬렉션 완전 삭제
        service.vector_store.delete_collection()

        # 새 컬렉션 생성
        new_collection = service.vector_store.client.get_or_create_collection(
            name="clothes", metadata={"hnsw:space": "cosine"}
        )

        # [핵심] 모든 서비스가 새 컬렉션을 바라보도록 업데이트해줘야 합니다!
        service.vector_store.collection = new_collection
        service.clothing_service.vector_store.collection = new_collection

        print(">> 벡터DB 초기화 및 연결 업데이트 완료")
    except Exception as e:
        print(f">> 초기화 건너뜀 또는 오류: {e}")

    # 4. 날씨 정보 출력
    if kma_key:
        print(">> 현재 날씨 정보 조회 중...")
        weather = service.get_weather("서울")
        if weather:
            print(f">> {weather.to_description()}")

    # 5. 옷 개수 확인 및 샘플 추가
    try:
        clothes_count = service.clothing_service.count()
    except:
        clothes_count = 0

    if clothes_count == 0:
        print(">> 등록된 옷이 없습니다. 샘플 데이터를 추가합니다...")
        added = insert_sample_clothes()
        print(f">> 샘플 옷 {added}개 추가 완료!")

    # 6. 벡터DB 동기화 (이제 32개가 정상적으로 들어가야 합니다)
    print(">> 벡터DB 동기화 중...")
    sync_result = service.clothing_service.sync_to_vector_db()
    print(f">> 동기화 완료 (새로 추가: {sync_result['synced']}개)")
    print()

    print("명령어: [질문 입력], 'list', 'weather', 'quit'")
    print("-" * 50)

    while True:
        try:
            user_input = input("\n[질문] ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["quit", "exit", "q", "종료"]:
                break

            if user_input.lower() == "list":
                clothes = service.clothing_service.get_all_clothes()
                print(f"\n[등록된 옷 목록] ({len(clothes)}벌)")
                for cloth in clothes:
                    print(f"  - [{cloth.category.value}] {cloth.name}")
                continue

            if user_input.lower() == "weather":
                if not kma_key:
                    print("기상청 API 키가 설정되지 않았습니다.")
                    continue

                # 1. 날씨 정보 가져오기
                weather = service.get_weather("서울")
                if weather:
                    print(f"\n[실시간 날씨 정보]")
                    print("-" * 30)
                    print(f"{weather.to_description()}")
                    print(f"추천 계절: {weather.get_season()}")
                else:
                    print("날씨 정보를 가져올 수 없습니다.")
                continue

            # 코디 추천 실행
            print("\n[코디 추천]")
            print("-" * 30)
            result = service.recommend_outfit(user_input)
            print(result)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"오류 발생: {e}")


if __name__ == "__main__":
    run_demo()
