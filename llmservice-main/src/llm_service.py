#API 호출 및 기능 구현 
from google import genai # 이걸 검색해야 클라이언트가 딸려오고 response 안에 뭐가 들어 있는지 확인 
from typing import Optional,List, Dict, Any

#시스템 프롬프트 
# LLM의 역할과 행동지침을 설정하는 부분
DEFAULT_SYSTEM_PROMPT = """ 
당신은 친절한 코디네이터 입니다. 
사용자의 질문에 맞는 의상을 추천하고 왜 그 의상을 추천하는지 설명해주세요. 
답변은 자연스럽고 친근하게 해주세요 
"""

class LLMService:
  """Gemini API 사용하여 텍스트 생성 서비스"""

  '''LLM 서비스 초기화'''
  def __init__(
      self, 
      api_key:str,
      model:str ="gemini-2.5-flash",
      system_prompt: Optional[str] = None):
    self.api_key = api_key
    self.model = model
    self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
    self.client = genai.Client(api_key=self.api_key) #클라이언트라는 키에다 , gemini에서 클라이언트가 있는데 , 재미나이 클라이언트 API에 self.api._key를 집어넣어준다. 재미나이에게 요청을 하도록 처리 
    
  '''프롬프트에 대한 응답을 생성'''
  def generate(self, prompt: str) ->str:
    #시스템 프롬프트와 사용자의 질문을 하나의 문자열로 합치기
    full_prompt = f"{self.system_prompt}\n\nUser: {prompt}"
    try:
      response = self.client.models.generate_content(
        model=self.model,
        contents=full_prompt)
      #모델이 생성한 최종 텍스트 
      if response.text:
        return response.text
      # 모델이 생성한 후보가 존재하는 경우 첫번재 후보의 텍스트 
      elif response.candidates:
        return response.candidates[0].content.parts[0].text 
      else:
        return "죄송합니다. 응답이 없습니다."
      
    except Exception as e:
      print(f"LLM응답 생성 오류 : {e}") #콘솔 로그 
      return f"응답 생성 중 오류가 발생햇습니다 잠시후 다시 시도해주세요." #화면에 나오는 것 

  #DB에서 찾아낸 데이터를 주입을 시켜야 함.
  # 추천 답변 Text 반환을 해야 한다. str로 반환값 고정 
  def generate_recommendation(
      self, 
      query:str,
      context_items:List[Dict[str,Any]]
      )->str:
    # DB에서 찾아낸 데이터를 LLM이 읽을 수 있는 문자열 형태로 변환
    context_str = self.format_context(context_items)

    #LLM에 DB에서 찾은 상품 정보 + 사용자의 원래 질문을 함께 제공하여 
    #주어진 정보 안에서 답변하도록 유도 -> 환각 현상 방지 
    prompt = f"""다음은 사용자 질문과 관련된 의상 정보 입니다 : {context_str}
사용자의 질문 : {query}
위 의상 정보를 참고하여 30살 남성 사용자에게 적절한 추천을 해주세요, 추천할 만한 것이 없다면 , 추가적으로 구매를 하면 좋은 옷들이랑 가격들도 같이 알려주세요  """
    return self.generate(prompt)



  def format_context(self, items:List[Dict[str,Any]]) -> str:
    #결과를 한줄씩 추가할 리스트를 만들어준것 . 
    lines = []
    #enumerate : 데이터와 순서(index)를 동시에 가져오기 
    for idx,item in enumerate(items,start=1):
     #딕셔너리 내부의 {키: 값} 쌍들을 "키:값" 형태의 문자열로 변경
     # 값이 여러개라면 중간에 ,로 구분하여 연결 하도록 하겟다.
     item_info = ",".join(f"{key}:{value}" for key,value in item.items())
     # 결과 예시 : 1. 카테고리 : 상의, 색상: 검정 .. 인덱스 이용해서 각각 의상의 숫자를 넣어줌.
     lines.append(f"{idx}. {item_info}")
     #lines 리스트에 담긴 모든 아이템 문자열을 합쳐서 하나의 긴 문자열로 반환
    return "\n".join(lines)
  