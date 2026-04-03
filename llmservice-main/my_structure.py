# 파이썬 스크립트를 이용하여 파이썬 프로젝트 생성 자동화
# 나만의 툴 만들기
import os

def create_project_structure():
    #만들고자 하는 폴더 리스트
    folders = ['src/database', 'src/models','tests','scripts']

    #만들고자 하는 파일 리스트
    files = ['src/__init__.py',
             'src/clothing_service.py',
             'src/llm_service.py',
             'src/rag_pipeline.py',
             'main.py',
             '.gitignore',
             'README.md',
             'requirements.txt']

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"폴더 생성 완료 : {folder}")

    for file in files:
        with open(file, "w", encoding="utf-8") as f:
            f.write("# 파일 생성 완료");
        print(f"파일 생성 완료 : {file}")

if __name__ == "__main__":
    create_project_structure()
    print("프로젝트 구조 생성 완료")