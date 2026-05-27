import streamlit as st
import time

# 1. 웹페이지 기본 설정 (웹브라우저 탭에 표시될 내용)
st.set_page_config(
    page_title="나의 MBTI 포켓몬 찾기! 🔮",
    page_icon="🦄",
    layout="centered"
)

# 2. MBTI와 포켓몬 매칭 데이터 (딕셔너리 구조)
mbti_pokemon = {
    "ISTJ": {"name": "이상해씨 (Bulbasaur)", "emoji": "🍃", "desc": "신중하고 책임감 강한 당신은 언제나 믿음직스러운 이상해씨와 닮았어요! 묵묵히 자기 할 일을 해내는 멋진 사람입니다.", "type": "풀 / 독"},
    "ISFJ": {"name": "메가니움 (Meganium)", "emoji": "🌸", "desc": "온화하고 헌신적인 당신은 주변을 편안하게 만들어주는 메가니움 타입! 다른 사람을 배려하는 따뜻한 마음을 가졌어요.", "type": "풀"},
    "INFJ": {"name": "뮤 (Mew)", "emoji": "✨", "desc": "신비롭고 깊은 통찰력을 지닌 당신은 전설의 포켓몬 뮤와 닮았어요! 조용하지만 세상을 바꾸는 따뜻한 신념이 있답니다.", "type": "에스퍼"},
    "INTJ": {"name": "메타그로스 (Metagross)", "emoji": "🤖", "desc": "철저한 계획과 두뇌 회전이 빠른 당신은 지적인 메타그로스 타입! 어떤 문제든 논리적으로 해결해 나가는 해결사군요.", "type": "강철 / 에스퍼"},
    "ISTP": {"name": "개굴닌자 (Greninja)", "emoji": "🐸", "desc": "냉철하고 상황 적응력이 뛰어난 당신은 쿨한 개굴닌자와 닮았어요! 과묵하지만 필요할 때 엄청난 능력을 발휘해요.", "type": "물 / 악"},
    "ISFP": {"name": "이브이 (Eevee)", "emoji": "🦊", "desc": "자유롭고 예술적 감각이 풍부한 당신은 무한한 가능성을 가진 이브이! 다정다감하고 매력적인 분위기를 풍깁니다.", "type": "노말"},
    "INFP": {"name": "푸린 (Jigglypuff)", "emoji": "🎈", "desc": "풍부한 감수성과 낭만을 품은 당신은 귀여운 푸린과 닮았어요! 예술적이고 마음이 여리며 상상력이 풍부합니다.", "type": "노말 / 페어리"},
    "INTP": {"name": "로토무 (Rotom)", "emoji": "⚡", "desc": "호기심이 많고 분석적인 당신은 전자기기를 자유자재로 넘나드는 로토무 타입! 독창적인 생각으로 세상을 탐구합니다.", "type": "전기 / 고스트"},
    "ESTP": {"name": "윈디 (Arcanine)", "emoji": "🔥", "desc": "모험을 즐기고 에너지가 넘치는 당신은 늠름하고 빠른 윈디와 닮았어요! 활동적이고 직관적이며 순간을 즐길 줄 압니다.", "type": "불꽃"},
    "ESFP": {"name": "토게피 (Togepi)", "emoji": "🥚", "desc": "인싸 중의 인싸, 분위기 메이커인 당신은 모두에게 행복을 주는 토게피! 매사 긍정적이고 사람들을 즐겁게 만듭니다.", "type": "페어리"},
    "ENFP": {"name": "피카츄 (Pikachu)", "emoji": "⚡️", "desc": "발랄하고 활기찬 에너지가 가득한 당신은 사랑스러운 피카츄와 닮았어요! 창의적이고 사람들과 어울리는 것을 정말 좋아해요.", "type": "전기"},
    "ENTP": {"name": "팬텀 (Gengar)", "emoji": "😈", "desc": "장난기 넘치고 재치 있는 당신은 위트 가득한 팬텀 타입! 독창적인 아이디어와 유머로 사람들을 깜짝 놀라게 만듭니다.", "type": "고스트 / 독"},
    "ESTJ": {"name": "괴력몬 (Machamp)", "emoji": "💪", "desc": "지도력이 있고 질서를 중시하는 당신은 든든한 괴력몬과 닮았어요! 목표를 향해 정진하며 집단을 이끄는 리더십이 돋보입니다.", "type": "격투"},
    "ESFJ": {"name": "해피너스 (Blissey)", "emoji": "💕", "desc": "친절하고 사교적인 당신은 모두에게 행복과 치유를 선물하는 해피너스! 주변 사람들의 고민을 잘 들어주는 따뜻한 수호천사예요.", "type": "노말"},
    "ENFJ": {"name": "망나뇽 (Dragonite)", "emoji": "🐉", "desc": "정의롭고 리더십이 뛰어나며 마음도 넓은 당신은 망나뇽 타입! 선한 영향력을 널리 퍼뜨려 사람들을 이끄는 리더입니다.", "type": "드래곤 / 비행"},
    "ENTJ": {"name": "리자몽 (Charizard)", "emoji": "🔥", "desc": "대담하고 목표 지향적인 당신은 열정적인 리자몽과 닮았어요! 카리스마 넘치는 리더십으로 목표를 반드시 이루어내고 마는 멋진 사람입니다.", "type": "불꽃 / 비행"}
}

# 3. 메인 화면 꾸미기
st.title("🔮 내 MBTI에 어울리는 포켓몬은?")
st.write("간단하게 나의 MBTI를 선택하고, 나와 찰떡궁합인 포켓몬 친구를 만나보세요! 🎈")

st.markdown("---")

# 4. 입력창 및 상호작용
# selectbox를 사용하여 MBTI 리스트를 선택할 수 있게 합니다.
mbti_list = sorted(list(mbti_pokemon.keys()))
selected_mbti = st.selectbox("👇 당신의 MBTI를 선택해 주세요!", mbti_list, index=0)

# 결과 확인 버튼
if st.button("내 포켓몬 확인하기 🐾", use_container_width=True):
    # 재미를 위한 스피너(로딩 애니메이션) 추가
    with st.spinner('당신과 닮은 포켓몬을 분석하는 중... ⏱️'):
        time.sleep(1.5)  # 1.5초 대기 효과
    
    # 선택된 MBTI에 맞는 데이터 가져오기
    pokemon = mbti_pokemon[selected_mbti]
    
    # 화면 축하 효과 (풍선 팡팡!)
    st.balloons()
    
    # 결과 화면 출력
    st.success(f"🎉 분석 완료! 당신의 매칭 포켓몬은 바로...")
    
    # 예쁘게 디자인된 카드 형태로 결과 출력
    st.markdown(
        f"""
        <div style="
            background-color: #f0f2f6; 
            padding: 20px; 
            border-radius: 15px; 
            border-left: 5px solid #ff4b4b;
            margin-top: 10px;
            margin-bottom: 20px;">
            <h2 style="margin: 0;"> {pokemon['emoji']} {pokemon['name']}</h2>
            <p style="color: gray; font-size: 0.9em; margin-top: 5px;">타입: <b>{pokemon['type']}</b></p>
            <hr style="border: 0.5px solid #ccc; margin: 10px 0;">
            <p style="font-size: 1.1em; line-height: 1.6;">{pokemon['desc']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 소소한 조언 한마디 추가
    st.info(f"💡 **한 줄 팁:** {pokemon['name']}의 긍정적인 에너지를 받아 오늘 하루도 힘내세요! 🔥")

st.markdown("---")
st.caption("제작: 당곡고등학교 멋쟁이 개발자 학생 🎓 | Powered by Streamlit")
