import openai
import streamlit as st
from openai import OpenAI
import os

# 페이지 설정
st.set_page_config(
    page_title="🌍 Travel ChatGPT",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 스타일
st.markdown("""
<style>
    /* 메인 배경 */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* 제목 스타일 */
    .main-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* 사이드바 스타일 */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2C3E50 0%, #3498DB 100%);
    }
    
    /* 채팅 컨테이너 */
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* 사용자 메시지 */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        animation: slideInRight 0.3s ease-out;
    }
    
    /* AI 메시지 */
    .ai-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
        animation: slideInLeft 0.3s ease-out;
    }
    
    /* 애니메이션 */
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* 입력 박스 스타일 */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 12px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #764ba2;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
        transform: scale(1.02);
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 25px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* 사이드바 스타일 */
    .sidebar-title {
        color: #FFD700;
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* 경고 메시지 스타일 */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid #FF6B6B;
    }
    
    /* 메시지 아이콘 */
    .message-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 헤더 섹션
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-title">🌍 Travel ChatGPT ✈️</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: white; font-size: 1.2rem; margin-bottom: 2rem;">🗺️ 당신만의 여행 가이드와 대화하세요! 🧳</p>', unsafe_allow_html=True)

# 사이드바 설정
with st.sidebar:
    st.markdown('<h2 class="sidebar-title">⚙️ 설정</h2>', unsafe_allow_html=True)
    
    # API 키 입력
    openai_api_key = st.text_input(
        "🔑 OpenAI API 키", 
        type="password",
        placeholder="sk-..."
    )
    
    if not openai_api_key:
        st.warning("🚨 OpenAI API 키를 입력하세요.")
        st.info("💡 OpenAI 웹사이트에서 API 키를 발급받으세요.")
        st.stop()
    
    st.success("✅ API 키가 설정되었습니다!")
    
    # 추가 설정 옵션
    st.markdown("### 🎯 채팅 옵션")
    
    # 대화 초기화 버튼
    if st.button("🗑️ 대화 초기화", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", 
             "content": "당신은 여행에 관한 질문에 답하는 전문 챗봇입니다. "
                    "모든 답변은 반드시 한국어와 영어를 함께 제공해주세요. 예시: '서울은 한국의 수도입니다. (Seoul is the capital of South Korea.)' "
                    "여행 외의 질문에 대해서는 '죄송하지만 여행 관련 질문에만 답변드릴 수 있습니다. (Sorry, I can only answer travel-related questions.)'라고 답변하세요. "
                    "모르는 내용은 절대 만들어서 답하지 마세요. 확실하지 않은 정보는 '정확한 정보를 확인해보시기 바랍니다. (Please verify the accurate information.)'라고 안내하세요. "
                    "여행지 추천, 준비물, 문화, 음식 등 다양한 여행 주제에 대해 친절하게 한국어와 영어로 동시에 안내해주세요."
            }
        ]
        st.rerun()
    
    # 통계 정보
    if "messages" in st.session_state:
        message_count = len([msg for msg in st.session_state.messages if msg["role"] != "system"])
        st.markdown(f"### 📊 대화 통계")
        st.metric("💬 총 메시지 수", message_count)

# OpenAI 클라이언트 설정
client = OpenAI(api_key=openai_api_key)

# 초기 대화 상태 설정
if "messages" not in st.session_state:
    st.session_state.messages = [
       {"role": "system", 
         "content": "당신은 여행에 관한 질문에 답하는 전문 챗봇입니다. "
                "모든 답변은 반드시 한국어와 영어를 함께 제공해주세요. 예시: '서울은 한국의 수도입니다. (Seoul is the capital of South Korea.)' "
                "여행 외의 질문에 대해서는 '죄송하지만 여행 관련 질문에만 답변드릴 수 있습니다. (Sorry, I can only answer travel-related questions.)'라고 답변하세요. "
                "모르는 내용은 절대 만들어서 답하지 마세요. 확실하지 않은 정보는 '정확한 정보를 확인해보시기 바랍니다. (Please verify the accurate information.)'라고 안내하세요. "
                "여행지 추천, 준비물, 문화, 음식 등 다양한 여행 주제에 대해 친절하게 한국어와 영어로 동시에 안내해주세요."
                    }  ]

# 메인 채팅 영역
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# 대화 내용 표시 (system 메시지는 제외)
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] != "system":
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <span class="message-icon">👤</span><strong>You:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="ai-message">
                    <span class="message-icon">🤖</span><strong>Travel Assistant:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 입력 영역
st.markdown("### 💭 메시지 입력")
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "", 
        placeholder="여행에 관해 궁금한 것을 물어보세요... (예: 일본 여행 추천지는?)",
        key="user_input",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("🚀 전송", use_container_width=True)

# 메시지 전송 처리
if send_button and user_input:
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 로딩 스피너 표시
    with st.spinner('🤔 답변을 생각하고 있습니다...'):
        try:
            # OpenAI API 호출
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                temperature=0.7
            )
            
            # OpenAI 응답 추가
            response_message = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": response_message})
            
            # 페이지 새로고침으로 입력 필드 초기화
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ 오류가 발생했습니다: {str(e)}")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white; margin-top: 2rem;">
    <p>🌟 <strong>Travel ChatGPT</strong> - 당신의 여행을 더욱 특별하게 만들어드립니다! ✨</p>
    <p style="font-size: 0.8rem; opacity: 0.8;">Powered by OpenAI GPT-4o-mini 🚀</p>
</div>
""", unsafe_allow_html=True)
