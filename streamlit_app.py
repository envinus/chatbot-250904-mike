# openai, OpenAI: OpenAI API 호출을 위한 라이브러리
# streamlit: 웹 UI 프레임워크
# os: (현재 예제에서는 사용되지 않음) 환경 변수 접근 또는 파일 경로 처리 용도

import openai
import streamlit as st
from openai import OpenAI
import os

# Streamlit app
st.title("ChatGPT와 대화하기")

# 오른쪽 사이드바에 OpenAI API 키 입력란 추가
st.sidebar.title("설정")
openai_api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")

if not openai_api_key:
    st.sidebar.warning("OpenAI API 키를 입력하세요.")
    st.stop()

# client = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
client = OpenAI(api_key  = openai_api_key)

# 초기 대화 상태 설정
# Streamlit 앱은 새로고침마다 상태가 초기화되는데, st.session_state를 쓰면 
#   사용자별 세션에 데이터를 유지할 수 있음.
# st.session_state에는 여러 개의 변수를 자유롭게 지정하고 저장할 수 있음.
# 숫자, 문자열, 리스트(대화 이력 등) 저장 가능.
if "messages" not in st.session_state:
    st.session_state.messages = [
       {"role": "system", 
         "content": "당신은 여행에 관한 질문에 답하는 전문 챗봇입니다. "
                "모든 답변은 반드시 한국어와 영어를 함께 제공해주세요. 예시: '서울은 한국의 수도입니다. (Seoul is the capital of South Korea.)' "
                "여행 외의 질문에 대해서는 '죄송하지만 여행 관련 질문에만 답변드릴 수 있습니다. (Sorry, I can only answer travel-related questions.)'라고 답변하세요. "
                "모르는 내용은 절대 만들어서 답하지 마세요. 확실하지 않은 정보는 '정확한 정보를 확인해보시기 바랍니다. (Please verify the accurate information.)'라고 안내하세요. "
                "여행지 추천, 준비물, 문화, 음식 등 다양한 여행 주제에 대해 친절하게 한국어와 영어로 동시에 안내해주세요."
                    }  ]
# 사용자 입력
user_input = st.text_input("당신:", key="user_input")

if st.button("전송") and user_input:
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", 
                                      "content": user_input})

    # OpenAI API 호출
    response = client.chat.completions.create (
        model = "gpt-4o-mini",
        messages = st.session_state.messages
    )

    # OpenAI 응답 추가
    response_message = response.choices[0].message.content
    # st.session_state.messages.append(response_message)
    st.session_state.messages.append({"role": "assistant", 
                                      "content": response_message})

    # 사용자 입력 초기화
    user_input = ""

# 대화 내용 표시 (system 메시지는 제외)
for message in st.session_state.messages:
    if message["role"] != "system":  # system 메시지는 화면에 표시하지 않음
        icon = "👤"  if message["role"] == "user" else "🤖"
        st.markdown(f"{icon}: {message['content']}")
