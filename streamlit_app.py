import streamlit as st
from openai import OpenAI
import time

# 페이지 설정
st.set_page_config(
    page_title="🌍 Travel ChatGPT",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Material Design 기반 CSS 스타일
st.markdown("""
<style>
    /* Material Design 색상 팔레트 */
    :root {
        --md-primary: #1976D2;
        --md-primary-variant: #1565C0;
        --md-secondary: #03DAC6;
        --md-background: #E8EBF5;
        --md-surface: #FFFFFF;
        --md-surface-variant: #F5F5F5;
        --md-on-primary: #FFFFFF;
        --md-on-surface: #212121;
        --md-on-surface-variant: #757575;
        --md-outline: #E0E0E0;
        --md-shadow: rgba(0, 0, 0, 0.12);
    }
    
    /* 전체 배경 */
    .main {
        background-color: var(--md-background);
        padding: 0;
    }
    
    /* 앱바 (헤더) */
    .app-header {
        background-color: var(--md-primary);
        color: var(--md-on-primary);
        padding: 16px 24px;
        box-shadow: 0 2px 4px var(--md-shadow);
        margin: -1rem -1rem 2rem -1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .app-title {
        font-size: 20px;
        font-weight: 500;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .verified-icon {
        background: var(--md-secondary);
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }
    
    /* 사용자 메시지 (오른쪽 정렬) */
    .user-message-container {
        display: flex;
        justify-content: flex-end;
        margin: 16px 0;
    }
    
    .user-message {
        background: var(--md-primary);
        color: var(--md-on-primary);
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        max-width: 70%;
        font-size: 14px;
        line-height: 1.4;
        box-shadow: 0 1px 2px var(--md-shadow);
    }
    
    /* AI 메시지 (왼쪽 정렬) */
    .ai-message-container {
        display: flex;
        justify-content: flex-start;
        margin: 16px 0;
    }
    
    .ai-message {
        background: var(--md-surface-variant);
        color: var(--md-on-surface);
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        max-width: 70%;
        font-size: 14px;
        line-height: 1.4;
        box-shadow: 0 1px 2px var(--md-shadow);
        border: 1px solid var(--md-outline);
    }
    
    /* 플로팅 액션 버튼 스타일 */
    .stButton > button {
        background: var(--md-primary);
        color: var(--md-on-primary);
        border: none;
        border-radius: 24px;
        padding: 12px 24px;
        font-size: 14px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.2s cubic-bezier(0.4, 0.0, 0.2, 1);
        box-shadow: 0 2px 4px var(--md-shadow);
        min-height: 48px;
    }
    
    .stButton > button:hover {
        background: var(--md-primary-variant);
        box-shadow: 0 4px 8px var(--md-shadow);
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px var(--md-shadow);
    }
    
    /* 텍스트 입력 필드 */
    .stTextInput > div > div > input {
        background: var(--md-surface);
        border: 2px solid var(--md-outline);
        border-radius: 4px;
        padding: 16px;
        font-size: 16px;
        color: var(--md-on-surface);
        transition: border-color 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--md-primary);
        outline: none;
        box-shadow: 0 0 0 1px var(--md-primary);
    }
    
    /* 메인 콘텐츠 너비 조정 */
    .main .block-container {
        max-width: 1000px;
        padding: 2rem 1rem;
    }
    
    /* 칩 스타일 */
    .status-chip {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
    }
    
    .fact-chip {
        background: #E8F5E8;
        color: #2E7D32;
    }
    
    /* 정보 카드 */
    .info-card {
        background: var(--md-surface);
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
        border-left: 4px solid var(--md-primary);
        box-shadow: 0 1px 3px var(--md-shadow);
    }
    
    /* 메트릭 카드 */
    .metric-card {
        background: var(--md-surface);
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px var(--md-shadow);
        border: 1px solid var(--md-outline);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 500;
        color: var(--md-primary);
    }
    
    .metric-label {
        font-size: 14px;
        color: var(--md-on-surface-variant);
        margin-top: 4px;
    }
    
    /* 하단 액션 바 */
    .bottom-actions {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: var(--md-surface);
        padding: 16px 0;
        border-top: 1px solid var(--md-outline);
        box-shadow: 0 -2px 4px var(--md-shadow);
        z-index: 1000;
        display: flex;
        justify-content: center;
    }
    
    /* 로딩 바 스타일 */
    .loading-container {
        width: 100%;
        background-color: #f0f0f0;
        border-radius: 10px;
        margin: 20px 0;
        overflow: hidden;
    }
    
    .loading-bar {
        height: 8px;
        background: linear-gradient(90deg, var(--md-primary), var(--md-secondary));
        border-radius: 10px;
        animation: loading 2s ease-in-out infinite;
    }
    
    @keyframes loading {
        0% { width: 0%; }
        50% { width: 70%; }
        100% { width: 100%; }
    }
    
    .loading-text {
        text-align: center;
        color: var(--md-on-surface-variant);
        font-size: 14px;
        margin-top: 10px;
    }
    
    /* 스크롤바 숨기기 */
    .main::-webkit-scrollbar {
        width: 8px;
    }
    
    .main::-webkit-scrollbar-track {
        background: var(--md-background);
    }
    
    .main::-webkit-scrollbar-thumb {
        background: var(--md-outline);
        border-radius: 4px;
    }
    
    .main::-webkit-scrollbar-thumb:hover {
        background: var(--md-on-surface-variant);
    }
    
    /* 반응형 디자인 */
    @media (max-width: 768px) {
        .app-header {
            padding: 12px 16px;
        }
        
        .user-message, .ai-message {
            max-width: 85%;
        }
        
        .bottom-actions {
            padding: 12px;
        }
        
        .main .block-container {
            padding: 1rem 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div class="app-header">
    <div class="app-title">
        ✈️ Travel Assistant
        <div class="verified-icon">✓</div>
    </div>
    <div style="display: flex; gap: 8px;">
        <button style="background: none; border: none; color: white; padding: 8px;">⚙️</button>
        <button style="background: none; border: none; color: white; padding: 8px;">⋯</button>
    </div>
</div>
""", unsafe_allow_html=True)

# API 키 설정
openai_api_key = st.secrets["openai"]["API_KEY"]

# 대화 초기화 버튼
if st.button("🗑️ 대화 초기화"):
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

# 로딩 상태 관리
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

# 메인 대화 영역
st.markdown("### 💬 대화")

# 대화 내용 표시 (system 메시지는 제외)
messages_container = st.container()
with messages_container:
    for i, message in enumerate(st.session_state.messages):
        if message["role"] != "system":
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message-container">
                    <div class="user-message">
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="ai-message-container">
                    <div class="ai-message">
                        <div style="margin-bottom: 8px;">
                            <span class="status-chip fact-chip">Fact</span>
                        </div>
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# 로딩 바 표시
if st.session_state.is_loading:
    with st.spinner('💭 여행 전문가가 답변을 준비하고 있습니다...'):
        time.sleep(0.5)  # 로딩 애니메이션을 보여주기 위한 딜레이

# 입력 영역을 하단에 고정
st.markdown("<div style='margin-bottom: 120px;'></div>", unsafe_allow_html=True)

# 하단 고정 입력 영역
st.markdown("""
<div class="bottom-actions">
    <div style="max-width: 1200px; margin: 0 auto;">
""", unsafe_allow_html=True)

# Enter 키 입력을 위한 폼 사용
with st.form(key="message_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "", 
            placeholder="여행에 대해 궁금한 것을 물어보세요... (Enter로 전송)",
            key="user_input_form",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.form_submit_button("전송", use_container_width=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# 메시지 전송 처리
if send_button and user_input and not st.session_state.is_loading:
    # 로딩 상태 시작
    st.session_state.is_loading = True
    
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 페이지 새로고침하여 로딩 바 표시
    st.rerun()

# 실제 API 호출 (로딩 상태일 때)
if st.session_state.is_loading:
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
        
        # 로딩 상태 종료
        st.session_state.is_loading = False
        
        # 페이지 새로고침
        st.rerun()
        
    except Exception as e:
        st.session_state.is_loading = False
        st.error(f"❌ 오류가 발생했습니다: {str(e)}")
        st.rerun()
