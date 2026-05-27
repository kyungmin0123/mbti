import streamlit as st
import time
import random

# 1. 페이지 설정
st.set_page_config(
    page_title="포켓몬 MBTI 소환 센터 🔮",
    page_icon="⚡",
    layout="centered"
)

# 2. 울트라 고퀄리티 비주얼 스타일 (CSS)
st.markdown("""
    <style>
    /* 전체 배경: 은은한 사이버 파스텔 그라데이션 */
    [data-testid="stAppViewContainer"], .stApp {
        background: linear-gradient(135deg, #FFE5EC 0%, #F0E6FF 50%, #E8F0FE 100%) !important;
        background-attachment: fixed;
    }
    
    /* 헤더 카드 글래스모피즘 효과 */
    .header-box {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(100, 110, 220, 0.15);
        border: 3px solid #4EA8DE;
        text-align: center;
        margin-bottom: 25px;
    }
    
    .title-text {
        font-size: 2.3em !important;
        font-weight: 900;
        color: #2B2D42;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        margin-bottom: 5px;
    }

    /* 결과 카드 기본형 */
    .result-card {
        background: white !important;
        padding: 25px;
        border-radius: 25px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
        border: 4px solid #4EA8DE;
        margin-top: 15px;
        transition: transform 0.3s;
    }
    
    /* 이로치(Shiny) 획득 시 테두리 황금빛 번쩍임 애니메이션 */
    .shiny-card {
        background: linear-gradient(white, white) padding-box,
                    linear-gradient(135deg, #FFD700, #FFA500, #FF4500) border-box !important;
        padding: 25px;
        border-radius: 25px;
        box-shadow: 0 20px 45px rgba(255, 165, 0, 0.4);
        border: 4px solid transparent;
        margin-top: 15px;
        animation: shiny-glow 2s infinite alternate;
    }

    @keyframes shiny-glow {
        0% { box-shadow: 0 0 15px #FFD700; }
        100% { box-shadow: 0 0 35px #FF4500; }
    }

    /* 능력치 레이블 스타일 */
    .stat-label {
        font-weight: bold;
        color: #4A4A4A;
        font-size: 0.9em;
    }

    .footer {
        text-align: center;
        color: #6C757D;
        font-size: 0.85em;
        margin-top: 50px;
        padding: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 고화질 이미지 번호 및 게임 종족값(HP, 공격, 방어, 스피드) 정밀 데이터 세팅
mbti_pokemon = {
    "ISTJ": {
        "name": "이상해씨 (Bulbasaur)", "id": 1, "emoji": "🍃", "type": "풀 / 독", "partner": "ESFP",
        "stats": {"HP": 45, "공격": 49, "방어": 49, "스피드": 45},
        "desc": "신중하고 책임감이 강하며 계획적인 당신은 성실함의 대명사 '이상해씨'와 똑 닮았어요! 규칙과 질서를 지키며 조용히 자신의 자리를 빛내는 멋진 사람입니다."
    },
    "ISFJ": {
        "name": "메가니움 (Meganium)", "id": 154, "emoji": "🌸", "type": "풀", "partner": "ESTP",
        "stats": {"HP": 80, "공격": 82, "방어": 100, "스피드": 80},
        "desc": "온화하고 헌신적이며 주변 사람들의 기분을 세심하게 살피는 당신은 '메가니움' 타입! 타인에게 조건 없는 신뢰와 따뜻함을 선사하는 천사 같은 마음씨를 가졌어요."
    },
    "INFJ": {
        "name": "뮤 (Mew)", "id": 151, "emoji": "✨", "type": "에스퍼", "partner": "ENFP",
        "stats": {"HP": 100, "공격": 100, "방어": 100, "스피드": 100},
        "desc": "신비롭고 깊은 통찰력을 가졌으며, 강한 신념과 상상력을 가진 당신은 전설의 포켓몬 '뮤'를 닮았습니다. 세상을 따뜻하고 의미 있게 만드려는 꿈을 마음속에 품고 살아가요."
    },
    "INTJ": {
        "name": "메타그로스 (Metagross)", "id": 376, "emoji": "🤖", "type": "강철 / 에스퍼", "partner": "ENTP",
        "stats": {"HP": 80, "공격": 135, "방어": 130, "스피드": 70},
        "desc": "논리적이고 독립적이며, 어떤 문제든 완벽하게 분석해 내는 전략가인 당신은 똑똑한 컴퓨터 포켓몬 '메타그로스' 타입! 목표가 생기면 무서운 집중력으로 해결책을 도출합니다."
    },
    "ISTP": {
        "name": "개굴닌자 (Greninja)", "id": 658, "emoji": "🐸", "type": "물 / 악", "partner": "ESFJ",
        "stats": {"HP": 72, "공격": 95, "방어": 67, "스피드": 122},
        "desc": "말은 적지만 상황 판단력이 매우 뛰어나고 위기 대처에 강한 당신은 쿨한 매력의 '개굴닌자'와 닮았어요! 도구를 다루는 손재주와 쿨한 자유로움이 매력 포인트입니다."
    },
    "ISFP": {
        "name": "이브이 (Eevee)", "id": 133, "emoji": "🦊", "type": "노말", "partner": "ESTJ",
        "stats": {"HP": 55, "공격": 55, "방어": 50, "스피드": 55},
        "desc": "예술적 감수성이 풍부하고 유연한 사고방식을 가진 따뜻한 영혼의 소유자! 다양한 속성으로 진화할 수 있는 '이브이'처럼 무한한 잠재력과 다정함을 품고 있습니다."
    },
    "INFP": {
        "name": "푸린 (Jigglypuff)", "id": 39, "emoji": "🎈", "type": "노말 / 페어리", "partner": "ENFJ",
        "stats": {"HP": 115, "공격": 45, "방어": 20, "스피드": 20},
        "desc": "풍부한 상상력과 로맨틱한 마음, 따뜻한 동정심을 지닌 평화주의자인 당신은 사랑스러운 '푸린' 타입! 가끔은 엉뚱하지만 사람들의 마음을 치유해 주는 깊은 감정을 가지고 있어요."
    },
    "INTP": {
        "name": "로토무 (Rotom)", "id": 479, "emoji": "⚡", "type": "전기 / 고스트", "partner": "ENTJ",
        "stats": {"HP": 50, "공격": 50, "방어": 77, "스피드": 91},
        "desc": "호기심이 끊이지 않고, 독창적인 아이디어와 비평적인 분석을 즐기는 아이디어 뱅크! 다채로운 가전제품에 들어가 변신하는 '로토무'처럼 지적 탐구심이 넘치는 사람입니다."
    },
    "ESTP": {
        "name": "윈디 (Arcanine)", "id": 59, "emoji": "🔥", "type": "불꽃", "partner": "ISFJ",
        "stats": {"HP": 90, "공격": 110, "방어": 80, "스피드": 95},
        "desc": "에너지가 넘치고 상황 적응력이 매우 뛰어나며 문제를 행동으로 해결해 나가는 당신은 달리는 폭풍 '윈디'와 닮았어요! 시원시원하고 털털한 성격으로 주변 사람들을 리드합니다."
    },
    "ESFP": {
        "name": "토게피 (Togepi)", "id": 175, "emoji": "🥚", "type": "페어리", "partner": "ISTJ",
        "stats": {"HP": 35, "공격": 20, "방어": 65, "스피드": 20},
        "desc": "인생을 축제처럼 즐길 줄 알고 주변에 항상 긍정적인 비타민 에너지를 발산하는 분위기 메이커! 보는 사람마다 미소 짓게 만드는 사랑둥이 포켓몬 '토게피'의 기운을 품고 계시네요."
    },
    "ENFP": {
        "name": "피카츄 (Pikachu)", "id": 25, "emoji": "⚡️", "type": "전기", "partner": "INFJ",
        "stats": {"HP": 35, "공격": 55, "방어": 40, "스피드": 90},
        "desc": "기발한 상상력, 사교적인 에너지, 그리고 미소를 부르는 밝은 매력의 소유자인 당신은 만인의 사랑을 받는 '피카츄' 타입! 지루할 틈 없이 세상을 모험하는 것을 좋아합니다."
    },
    "ENTP": {
        "name": "팬텀 (Gengar)", "id": 94, "emoji": "😈", "type": "고스트 / 독", "partner": "INTJ",
        "stats": {"HP": 60, "공격": 65, "방어": 60, "스피드": 110},
        "desc": "지적인 모험심과 위트, 장난기 넘치는 눈빛으로 토론과 논쟁을 즐기는 천재 발명가 타입! 예측 불가한 매력과 유쾌한 입담을 가진 장난꾸러기 '팬텀'이 당신과 딱 맞습니다."
    },
    "ESTJ": {
        "name": "괴력몬 (Machamp)", "id": 68, "emoji": "💪", "type": "격투", "partner": "ISFP",
        "stats": {"HP": 90, "공격": 130, "방어": 80, "스피드": 55},
        "desc": "철저한 계획과 뛰어난 추진력으로 일을 완벽하게 마무리하는 타고난 행정가! 듬직한 네 개의 팔로 성실히 팀을 이끄는 '괴력몬'처럼 든든한 리더십의 소유자입니다."
    },
    "ESFJ": {
        "name": "해피너스 (Blissey)", "id": 242, "emoji": "💕", "type": "노말", "partner": "ISTP",
        "stats": {"HP": 255, "공격": 10, "방어": 10, "스피드": 55},
        "desc": "주변 사람들을 살뜰히 챙기고 정이 넘치며 뛰어난 공감 능력을 가진 따뜻한 친절왕! 아픈 포켓몬을 치료해 주는 '해피너스'처럼 언제나 주위 사람들을 감싸 안아주는 고마운 존재예요."
    },
    "ENFJ": {
        "name": "망나뇽 (Dragonite)", "id": 149, "emoji": "🐉", "type": "드래곤 / 비행", "partner": "INFP",
        "stats": {"HP": 91, "공격": 134, "방어": 95, "스피드": 80},
        "desc": "선한 영향력과 깊은 배려심으로 타인을 돕고 소통하는 따뜻한 리더! 폭풍우 치는 바다에서 조난자를 돕는 착하고 듬직한 전설의 드래곤 '망나뇽'과 가장 흡사합니다."
    },
    "ENTJ": {
        "name": "리자몽 (Charizard)", "id": 6, "emoji": "🔥", "type": "불꽃 / 비행", "partner": "INTP",
        "stats": {"HP": 78, "공격": 84, "방어": 78, "스피드": 100},
        "desc": "야망이 넘치며 비전을 달성하기 위해 강력한 카리스마로 대중을 리드하는 불꽃 같은 열정가! 압도적인 위엄과 강인함을 가진 뜨거운 드래곤 '리자몽'처럼 도전을 무서워하지 않습니다."
    }
}

# 4. 헤더 대문
st.markdown("""
    <div class="header-box">
        <div class="title-text">🔮 전설의 MBTI 포켓몬 매칭 센터</div>
        <p style="color: #4A5568; font-size: 1.1em; margin: 8px 0 0 0;">
            오리지널 울음소리 🔊 와 희귀 이로치 찬스 ✨가 있는 모험을 시작해보세요!
        </p>
    </div>
""", unsafe_allow_html=True)

# 5. [추가기능 1] MBTI를 모르는 친구를 위한 간이 자가진단 (Expander)
with st.expander("🤔 내 MBTI를 잘 모르겠나요? (초간단 4문항 테스트)"):
    st.write("간단하게 선택해 주시면 본인의 MBTI가 자동 계산되어 메인 선택창에 적용됩니다!")
    q1 = st.radio("1. 에너지를 어디서 얻나요?", ["사람들과 수다 떨고 활동할 때 (E)", "조용히 혼자 쉬거나 충전할 때 (I)"], index=0)
    q2 = st.radio("2. 정보를 파악하는 방식은?", ["오감과 사실적인 현실에 집중 (S)", "육감과 미래의 상상, 가능성에 집중 (N)"], index=1)
    q3 = st.radio("3. 결정을 내릴 때 중요한 것은?", ["논리와 객관적인 분석이 우선 (T)", "사람 간의 관계와 감정 공감이 우선 (F)"], index=0)
    q4 = st.radio("4. 생활하는 패턴은?", ["계획적이고 체계적인 실천 (J)", "상황에 맞춰 즉흥적으로 움직임 (P)"], index=1)
    
    # MBTI 스트링 계산
    calc_mbti = (
        ("E" if "E" in q1 else "I") +
        ("S" if "S" in q2 else "N") +
        ("T" if "T" in q3 else "F") +
        ("J" if "J" in q4 else "P")
    )
    st.success(f"당신의 추천 MBTI는 **{calc_mbti}** 입니다! 아래 선택창에 적용 버튼을 눌러보세요.")
    if st.button("내 MBTI 적용하기 🎯"):
        st.session_state["my_mbti"] = calc_mbti
        st.toast(f"{calc_mbti}가 적용되었습니다!")

# 6. 메인 입력창 설정
mbti_list = sorted(list(mbti_pokemon.keys()))
default_mbti = st.session_state.get("my_mbti", "ENFP") # 간이 테스트 연동

col1, col2 = st.columns([2, 1])
with col1:
    selected_mbti = st.selectbox("👇 분석할 MBTI를 골라주세요!", mbti_list, index=mbti_list.index(default_mbti))
with col2:
    # 이로치 강제 소환 치트키 스위치!
    force_shiny = st.checkbox("✨ 무조건 이로치 소환!")

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# 7. 소환 개시!
if st.button("☄️ 포켓볼 던지기!! (소환) ☄️", use_container_width=True):
    
    # 7-1. 극적인 로딩 효과
    with st.spinner('정령 소환중... 포켓볼이 흔들립니다! 🔴'):
        time.sleep(1.2)
    
    # 7-2. 이로치 확률 연산 (치트키 켜져있거나 10% 확률 돌입 시)
    is_shiny = force_shiny or (random.random() < 0.10)
    
    pokemon = mbti_pokemon[selected_mbti]
    partner_mbti = pokemon["partner"]
    partner_pokemon = mbti_pokemon[partner_mbti]
    
    # 7-3. PokeAPI 공식 고해상도 이미지 (이로치 여부에 따라 디렉토리 변경)
    if is_shiny:
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/{pokemon['id']}.png"
        st.balloons()
        st.toast("✨ 와우! 10%의 확률을 뚫고 '색이 다른' 이로치 포켓몬이 소환되었습니다!! ✨")
    else:
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon['id']}.png"
        st.snow() # 일반 소환 시 눈 내리는 은은한 효과
        
    # 7-4. 울음소리 오디오 파일 URL 연동 (PokeAPI 공식 소리 데이터베이스)
    cry_url = f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{pokemon['id']}.ogg"
    
    # 7-5. 소리를 웹 화면에 몰래 재생하기 (audio autoplay, 화면엔 숨김)
    st.markdown(f'<audio src="{cry_url}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
    
    # 8. 소환 성공 카드 레이아웃 구성
    card_style = "shiny-card" if is_shiny else "result-card"
    
    st.markdown(f"<div class='{card_style}'>", unsafe_allow_html=True)
    
    c_col1, c_col2 = st.columns([1, 1.2])
    
    with c_col1:
        # 포켓몬 일러스트 전시
        st.image(image_url, use_container_width=True)
        # 이로치 타이틀 보너스 마크
        if is_shiny:
            st.markdown("<p style='text-align:center; color:#FF8C00; font-weight:bold; font-size:1.1em;'>✨ SHINY VERSION ✨</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='text-align:center; color:gray; font-size:0.9em;'>도감번호 No. {pokemon['id']}</p>", unsafe_allow_html=True)
            
    with c_col2:
        # 포켓몬 기본 정보
        st.markdown(f"### {pokemon['emoji']} {pokemon['name']}")
        st.markdown(f"<span class='pokemon-type'>타입: {pokemon['type']}</span>", unsafe_allow_html=True)
        st.write(pokemon['desc'])
        
        # [추가기능 2] 게임 능력치 스탯 바 표시 (Base Stats)
        st.markdown("<p style='margin-bottom:2px; font-weight:bold;'>🎮 포켓몬 성격 능력치</p>", unsafe_allow_html=True)
        for stat_name, stat_val in pokemon["stats"].items():
            # 실제 스탯을 프로그레스바로 시각화 (최대치 255 기준 비율 환산)
            normalized_val = min(1.0, stat_val / 150.0)
            col_stat1, col_stat2 = st.columns([1.5, 3.5])
            with col_stat1:
                st.markdown(f"<span class='stat-label'>{stat_name}: {stat_val}</span>", unsafe_allow_html=True)
            with col_stat2:
                # 스탯에 따라 바의 컬러를 다르게 적용하는 디테일
                color = "green" if stat_name == "HP" else "orange" if stat_name == "공격" else "blue"
                st.progress(normalized_val)
                
        # 환상의 궁합
        st.markdown(f"""
            <div class='partner-box'>
                🤝 <b>환상의 궁합:</b> {partner_mbti} ({partner_pokemon['name']})<br>
                <small>서로의 성격을 완벽히 보완해 주는 최고의 파트너 포켓몬입니다!</small>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

# 9. 푸터
st.markdown("""
    <div class="footer">
        💖 제작: 당곡고등학교 멋쟁이 개발자 학생 🎓 | Powered by Streamlit & PokeAPI
    </div>
""", unsafe_allow_html=True)
