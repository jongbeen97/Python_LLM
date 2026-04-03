import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 수정된 클래스들을 가져옵니다.
from src.weather_service import WeatherService, WeatherInfo


class TestWeatherService:

    @patch("src.weather_service.requests.get")
    def test_get_weather_success(self, mock_get):
        """1. 가짜 데이터를 이용한 API 응답 및 파싱 테스트"""
        # 가짜 응답 설정
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": {
                "header": {"resultCode": "00", "resultMsg": "NORMAL_SERVICE"},
                "body": {
                    "items": {
                        "item": [
                            {"category": "TMP", "fcstValue": "22.5"},  # 기온
                            {"category": "REH", "fcstValue": "45"},  # 습도
                            {"category": "WSD", "fcstValue": "1.5"},  # 풍속
                            {"category": "PTY", "fcstValue": "0"},  # 강수없음
                            {"category": "SKY", "fcstValue": "1"},  # 맑음
                        ]
                    }
                },
            }
        }
        mock_get.return_value = mock_response

        service = WeatherService(api_key="fake_key", endpoint="http://fake.api")
        weather = service.get_weather("서울")

        # 검증: 필드가 정확히 들어갔는지 확인
        assert weather is not None
        assert weather.temperature == 22.5
        assert weather.feels_like == pytest.approx(21.4)
        print(f"\nAPI 데이터 파싱 성공: {weather.to_description()}")

    def test_weather_logic_by_temperature(self):
        """2. 기온에 따른 계절 및 보온성 추천 로직 테스트"""
        # 케이스 A: 더운 여름 (26도)
        summer = WeatherInfo(26.0, 25.0, 60, "맑음", 1.0, "서울", False, False)
        assert summer.get_season() == "여름"
        assert summer.get_warmth() == (1, 2)

        # 케이스 B: 쌀쌀한 가을 (16도)
        fall = WeatherInfo(16.0, 15.0, 40, "맑음", 2.0, "서울", False, False)
        assert fall.get_season() == "가을"
        assert fall.get_warmth() == (3, 4)

        # 케이스 C: 추운 겨울 (5도)
        winter = WeatherInfo(5.0, 3.0, 30, "눈", 3.0, "서울", False, True)
        assert winter.get_season() == "겨울"
        assert winter.get_warmth() == (4, 5)
        print("\n계절/보온성 로직 검증 완료")

    def test_base_datetime_format(self):
        """3. 기준 시간 계산 결과의 형식 검증"""
        service = WeatherService(api_key="fake_key")
        date, time = service._get_base_datetime()

        # YYYYMMDD 형식(8자리)인지 확인
        assert len(date) == 8
        # HH00 형식(4자리)인지 확인
        assert len(time) == 4
        print(f"기준 시간 생성 확인: {date} {time}")


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
