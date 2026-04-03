"""옷 데이터 모델 정의"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime


class ClothingCategory(Enum):
    """옷 카테고리"""

    OUTER = "아우터"  # 코트, 자켓, 패딩 등
    TOP = "상의"  # 티셔츠, 셔츠, 니트 등
    BOTTOM = "하의"  # 바지, 스커트 등
    DRESS = "원피스"  # 원피스, 점프수트 등
    SHOES = "신발"  # 운동화, 구두 등
    ACCESSORY = "액세서리"  # 모자, 가방, 벨트 등


class Season(Enum):
    """계절"""

    SPRING = "봄"
    SUMMER = "여름"
    FALL = "가을"
    WINTER = "겨울"
    ALL = "사계절"


class Style(Enum):
    """스타일"""

    CASUAL = "캐주얼"
    FORMAL = "포멀"
    SPORTY = "스포티"
    STREET = "스트릿"
    MINIMAL = "미니멀"
    VINTAGE = "빈티지"
    CLASSIC = "클래식"


class Color(Enum):
    """색상"""

    BLACK = "블랙"
    WHITE = "화이트"
    GRAY = "그레이"
    NAVY = "네이비"
    BEIGE = "베이지"
    BROWN = "브라운"
    RED = "레드"
    BLUE = "블루"
    GREEN = "그린"
    YELLOW = "옐로우"
    PINK = "핑크"
    PURPLE = "퍼플"
    ORANGE = "오렌지"
    MULTI = "멀티컬러"


@dataclass
class Clothing:
    """옷 데이터 클래스"""

    id: int
    name: str
    category: ClothingCategory
    color: Color
    season: Season
    style: Style
    description: Optional[str] = None
    brand: Optional[str] = None
    image_url: Optional[str] = None
    warmth_level: int = 3  # 보온성 1(시원) ~ 5(따뜻)
    created_at: Optional[datetime] = None

    def to_text(self) -> str:
        """벡터 임베딩용 텍스트 생성"""
        parts = [
            f"{self.name}",
            f"카테고리: {self.category.value}",
            f"색상: {self.color.value}",
            f"계절: {self.season.value}",
            f"스타일: {self.style.value}",
            f"보온성: {'따뜻함' if self.warmth_level >= 4 else '보통' if self.warmth_level >= 2 else '시원함'}",
        ]
        if self.description:
            parts.append(f"설명: {self.description}")
        if self.brand:
            parts.append(f"브랜드: {self.brand}")
        return ", ".join(parts)

    def to_dict(self) -> dict:
        """딕셔너리로 변환 (벡터DB용 - None 값 제외)"""
        result = {
            "id": self.id,
            "name": self.name,
            "category": self.category.value,
            "color": self.color.value,
            "season": self.season.value,
            "style": self.style.value,
            "warmth_level": self.warmth_level,
        }
        # None이 아닌 값만 추가 (ChromaDB는 None 미지원)
        if self.description:
            result["description"] = self.description
        if self.brand:
            result["brand"] = self.brand
        if self.image_url:
            result["image_url"] = self.image_url
        if self.created_at:
            result["created_at"] = self.created_at.isoformat()
        return result
