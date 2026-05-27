import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(
    page_title="궁극의 MBTI 포켓몬 매칭 센터 🔮",
    page_icon="🌈",
    layout="centered"
)

# 2. ★ 대폭 업그레이드된 화려한 CSS 스타일 ★
# Streamlit의 기본 테마 배경을 덮어씌우고 귀여운 테마를 적용합니다.
st.markdown("""
    <style>
    /* 1. 전체 앱의 배경을 화사한 파스텔 그라데이션으로 변경 (피카츄 노란빛 + 푸른 하늘빛) */
    [data-testid="stAppViewContainer"], .stApp {
        background: linear-gradient(135deg, #FFF9D0 0%, #CAF0F8 50%, #E0AAFF 100%) !important;
        background-attachment: fixed;
    }
    
    /* 2. 메인 헤더를 투명하고 둥근 카드로 감싸기 (글래스모피즘 효과) */
    .header-box {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        border: 2px dashed #FFCB05; /* 포켓몬 공식 골드 색상의 점선 테두리 */
        text-align: center;
        margin-bottom: 25px;
    }
    
    /* 3. 메인 타이틀 텍스트 디자인 */
    .title-text {
        font-size: 2.2em !important;
        font-weight: 800;
        color: #1D3557;
        margin-bottom: 5px;
    }
    
    /* 4. 결과 출력용 고퀄리티 카드 디자인 */
    .result-card {
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 25px;
        border-radius: 24px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        border: 3px solid #FFDE00; /* 피카츄 옐로우 실선 테두리 */
        margin-top: 15px;
    }
    
    /* 5. 포켓몬 타입 라벨 */
    .pokemon-type {
        background-color: #EE1515; /* 포켓볼 레드 */
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85em;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    /* 6. 환상의 짝꿍 매칭 박스 */
    .partner-box {
        background-color: #E8F5E9;
        padding: 15px;
        border-radius: 15px;
        margin-top: 15px;
        border-left: 6px solid #4CAF50;
    }
    
    /* 7. 귀여운 푸터 영역 */
    .footer {
        text-align: center;
        color: #4A4A4A;
        font-size: 0.9em;
        margin-top: 40px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.4);
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 사전 정의 (PokeAPI의 공식 일러스트 ID 매핑)
mbti_pokemon = {
    "ISTJ": {
        "name": "이상해씨 (Bulbasaur)", "id": 1, "emoji": "🍃", "type": "풀 / 독", "partner": "ESFP",
        "desc": "신중하고 책임감이 강하며 계획적인 당신은 성실함의 대명사 '이상해씨'와 똑 닮았어요! 규칙과 질서를 지키며 조용히 자신의 자리를 빛내는 멋진 사람입니다."
    },
    "ISFJ": {
        "name": "메가니움 (Meganium)", "id": 154, "emoji": "🌸", "type": "풀", "partner": "ESTP",
        "desc": "온화하고 헌신적이며 주변 사람들의 기분을 세심하게 살피는 당신은 '메가니움' 타입! 타인에게 조건 없는 신뢰와 따뜻함을 선사하는 천사 같은 마음씨를 가졌어요."
    },
    "INFJ": {
        "name": "뮤 (Mew)", "id": 151, "emoji": "✨", "type": "에스퍼", "partner": "ENFP",
        "desc": "신비롭고 깊은 통찰력을 가졌으며, 강한 신념과 상상력을 가진 당신은 전설의 포켓몬 '뮤'를 닮았습니다. 세상을 따뜻하고 의미 있게 만드려는 꿈을 마음속에 품고 살아가요."
    },
    "INTJ": {
        "name": "메타그로스 (Metagross)", "id": 376, "emoji": "🤖", "type": "강철 / 에스퍼", "partner": "ENTP",
        "desc": "논리적이고 독립적이며, 어떤 문제든 완벽하게 분석해 내는 전략가인 당신은 똑똑한 컴퓨터 포켓몬 '메타그로스' 타입! 목표가 생기면 무서운 집중력으로 해결책을 도출합니다."
    },
    "ISTP": {
        "name": "개굴닌자 (Greninja)", "id": 658, "emoji": "🐸", "type": "물 / 악", "partner": "ESFJ",
        "desc": "말은 적지만 상황 판단력이 매우 뛰어나고 위기 대처에 강한 당신은 쿨한 매력의 '개굴닌자'와 닮았어요! 도구를 다루는 손재주와 쿨한 자유로움이 매력 포인트입니다."
    },
    "ISFP": {
        "name": "이브이 (Eevee)", "id": 133, "emoji": "🦊", "type": "노말", "partner": "ESTJ",
        "desc": "예술적 감수성이 풍부하고 유연한 사고방식을 가진 따뜻한 영혼의 소유자! 다양한 속성으로 진화할 수 있는 '이브이'처럼 무한한 잠재력과 다정함을 품고 있습니다."
    },
    "INFP": {
        "name": "푸린 (Jigglypuff)", "id": 39, "emoji": "🎈", "type": "노말 / 페어리", "partner": "ENFJ",
        "desc": "풍부한 상상력과 로맨틱한 마음, 따뜻한 동정심을 지닌 평화주의자인 당신은 사랑스러운 '푸린' 타입! 가끔은 엉뚱하지만 사람들의 마음을 치유해 주는 깊은 감정을 가지고 있어요."
    },
    "INTP": {
        "name": "로토무 (Rotom)", "id": 479, "emoji": "⚡", "type": "전기 / 고스트", "partner": "ENTJ",
        "desc": "호기심이 끊이지 않고, 독창적인 아이디어와 비평적인 분석을 즐기는 아이디어 뱅크! 다채로운 가전제품에 들어가 변신하는 '로토무'처럼 지적 탐구심이 넘치는 사람입니다."
    },
    "ESTP": {
        "name": "윈디 (Arcanine)", "id": 59, "emoji": "🔥", "type": "불꽃", "partner": "ISFJ",
        "desc": "에너지가 넘치고 상황 적응력이 매우 뛰어나며 문제를 행동으로 해결해 나가는 당신은 달리는 폭풍 '윈디'와 닮았어요! 시원시원하고 털털한 성격으로 주변 사람들을 리드합니다."
    },
    "ESFP": {
        "name": "토게피 (Togepi)", "id": 175, "emoji": "🥚", "type": "페어리", "partner": "ISTJ",
        "desc": "인생을 축제처럼 즐길 줄 알고 주변에 항상 긍정적인 비타민 에너지를 발산하는 분위기 메이커! 보는 사람마다 미소 짓게 만드는 사랑둥이 포켓몬 '토게피'의 기운을 품고 계시네요."
    },
    "ENFP": {
        "name": "피카츄 (Pikachu)", "id": 25, "emoji": "⚡️", "type": "전기", "partner": "INFJ",
        "desc": "기발한 상상력, 사교적인 에너지, 그리고 미소를 부르는 밝은 매력의 소유자인 당신은 만인의 사랑을 받는 '피카츄' 타입! 지루할 틈 없이 세상을 모험하는 것을 좋아합니다."
    },
    "ENTP": {
        "name": "팬텀 (Gengar)", "id": 94, "emoji": "😈", "type": "고스트 / 독", "partner": "INTJ",
        "desc": "지적인 모험심과 위트, 장난기 넘치는 눈빛으로 토론과 논쟁을 즐기는 천재 발명가 타입! 예측 불가한 매력과 유쾌한 입담을 가진 장난꾸러기 '팬텀'이 당신과 딱 맞습니다."
    },
    "ESTJ": {
        "name": "괴력몬 (Machamp)", "id": 68, "emoji": "💪", "type": "격투", "partner": "ISFP",
        "desc": "철저한 계획과 뛰어난 추진력으로 일을 완벽하게 마무리하는 타고난 행정가! 듬직한 네 개의 팔로 성실히 팀을 이끄는 '괴력몬'처럼 든든한 리더십의 소유자입니다."
    },
    "ESFJ": {
        "name": "해피너스 (Blissey)", "id": 242, "emoji": "💕", "type": "노말", "partner": "ISTP",
        "desc": "주변 사람들을 살뜰히 챙기고 정이 넘치며 뛰어난 공감 능력을 가진 따뜻한 친절왕! 아픈 포켓몬을 치료해 주는 '해피너스'처럼 언제나 주위 사람들을 감싸 안아주는 고마운 존재예요."
    },
    "ENFJ": {
        "name": "망나뇽 (Dragonite)", "id": 149, "emoji": "🐉", "type": "드래곤 / 비행", "partner": "INFP",
        "desc": "선한 영향력과 깊은 배려심으로 타인을 돕고 소통하는 따뜻한 리더! 폭풍우 치는 바다에서 조난자를 돕는 착하고 듬직한 전설의 드래곤 '망나뇽'과 가장 흡사합니다."
    },
    "ENTJ": {
        "name": "리자몽 (Charizard)", "id": 6, "emoji": "🔥", "type": "불꽃 / 비행", "partner": "INTP",
        "desc": "야망이 넘치며 비전을 달성하기 위해 강력한 카리스마로 대중을 리드하는 불꽃 같은 열정가! 압도적인 위엄과 강인함을 가진 뜨거운 드래곤 '리자몽'처럼 도전을 무서워하지 않습니다."
    }
}

# 4. 헤더 박스 영역
st.markdown("""
    <div class="header-box">
        <div class="title-text">🔮 나의 MBTI 포켓몬 매칭</div>
        <p style="color: #457B9D; font-size: 1.1em; margin: 10px 0 0 0;">
            환상적이고 귀여운 나만의 포켓몬 파트너를 찾으러 떠나볼까요? 🎈✈️
        </p>
    </div>
""", unsafe_allow_html=True)

# 5. 사용자 입력 선택
mbti_list = sorted(list(mbti_pokemon.keys()))

col_center = st.columns([1, 2, 1])
with col_center[1]:
    # selectbox도 둥글게 꾸며진 입력창
    selected_mbti = st.selectbox("👇 나의 MBTI 성격 유형 선택하기", mbti_list, index=0)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# 6. 매칭 분석 시작 버튼
if st.button("🌟 내 운명의 포켓몬 파트너 소환! 🌟", use_container_width=True):
    # 멋진 분석 대기 시각 효과
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)  # 신속하면서도 극적인 효과를 위해 1초 대기 효과
        progress_bar.progress(percent_complete + 1)
    
    pokemon = mbti_pokemon[selected_mbti]
    partner_mbti = pokemon["partner"]
    partner_pokemon = mbti_pokemon[partner_mbti]
    
    # 팡팡 터지는 꽃가루 효과!
    st.balloons()
    
    # 이미지 주소 생성 (PokeAPI 공식 깃허브 에셋)
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon['id']}.png"
    
    st.success(f"🎉 소환 완료! {selected_mbti} 유형의 파트너가 등장했습니다!")
    
    # 7. 세련된 결과 카드 레이아웃 출력
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    
    card_col1, card_col2 = st.columns([1, 1.2])
    
    with card_col1:
        # 좌측: 공식 포켓몬 고화질 일러스트 표시
        st.image(image_url, use_container_width=True)
        
    with card_col2:
        # 우측: 설명 및 상세 속성들
        st.markdown(f"### {pokemon['emoji']} {pokemon['name']}")
        st.markdown(f"<span class='pokemon-type'>타입: {pokemon['type']}</span>", unsafe_allow_html=True)
        st.write(pokemon['desc'])
        
        # 최고의 파트너 매치 정보 제공
        st.markdown(f"""
            <div class='partner-box'>
                🤝 <b>환상의 궁합 메이트:</b> {partner_mbti} ({partner_pokemon['name']})<br>
                <small>함께 모험을 떠나면 최고의 능력을 발휘할 수 있는 든든한 단짝입니다!</small>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.info(f"💡 **공유하기 꿀팁:** 친구들에게 나의 포켓몬 <b>{pokemon['name']}</b>을 소개하고, 친구들의 궁합 파트너도 확인해보세요!")

# 8. 푸터 영역 디자인
st.markdown("""
    <div class="footer">
        💛 당곡고등학교 멋쟁이 개발자 학생 🎓 | Powered by Streamlit & PokeAPI
    </div>
""", unsafe_allow_html=True)
