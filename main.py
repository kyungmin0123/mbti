import streamlit as st
import time
import random

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="움직이는 MBTI 포켓몬 소환소 🔮",
    page_icon="👾",
    layout="centered"
)

# 2. 러블리 파스텔 & 글래스모피즘 테마 CSS
st.markdown("""
    <style>
    /* 전체 배경: 아기자기한 솜사탕 파스텔 그라데이션 */
    [data-testid="stAppViewContainer"], .stApp {
        background: linear-gradient(135deg, #FFF0F5 0%, #E6F8FF 50%, #F3E8FF 100%) !important;
        background-attachment: fixed;
    }
    
    /* 헤더 카드 둥글고 예쁘게 꾸미기 */
    .header-box {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(12px);
        padding: 25px;
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(135, 206, 250, 0.2);
        border: 3px dashed #A2D2FF;
        text-align: center;
        margin-bottom: 25px;
    }
    
    .title-text {
        font-size: 2.2em !important;
        font-weight: 900;
        color: #1D3557;
        margin-bottom: 5px;
    }

    /* 포켓몬 카드 컨테이너 */
    .result-card {
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 25px;
        border-radius: 24px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
        border: 4px solid #BDE0FE;
        margin-top: 15px;
    }
    
    /* 이로치(Shiny) 당첨 시 무지갯빛 테두리 애니메이션 */
    .shiny-card {
        background: linear-gradient(white, white) padding-box,
                    linear-gradient(135deg, #FFD700, #FF6B6B, #FF8E53, #FFD700) border-box !important;
        padding: 25px;
        border-radius: 24px;
        box-shadow: 0 20px 45px rgba(255, 107, 107, 0.3);
        border: 4px solid transparent;
        margin-top: 15px;
        animation: rainbow-glow 3s infinite linear;
    }

    @keyframes rainbow-glow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }

    /* 능력치 글씨 꾸미기 */
    .stat-label {
        font-weight: bold;
        color: #495057;
        font-size: 0.85em;
    }

    /* 타입 배지 */
    .pokemon-type {
        background-color: #4EA8DE;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85em;
        display: inline-block;
        margin-bottom: 12px;
    }
    
    .partner-box {
        background-color: #F8F9FA;
        padding: 12px;
        border-radius: 12px;
        margin-top: 15px;
        border-left: 5px solid #FFC6FF;
    }

    .footer {
        text-align: center;
        color: #8E9AAF;
        font-size: 0.85em;
        margin-top: 45px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. MBTI 별 포켓몬 고유 도감 정보 및 상세 능력치
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
        "desc": "지적인 모험심 and 위트, 장난기 넘치는 눈빛으로 토론과 논쟁을 즐기는 천재 발명가 타입! 예측 불가한 매력과 유쾌한 입담을 가진 장난꾸러기 '팬텀'이 당신과 딱 맞습니다."
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

# 4. 헤더 대문 구성
st.markdown("""
    <div class="header-box">
        <div class="title-text">👾 생생하게 움직이는 MBTI 포켓몬</div>
        <p style="color: #4E878C; font-size: 1.1em; margin: 8px 0 0 0;">
            10%의 확률을 뚫고 찬란하게 빛나는 <b>이로치 포켓몬</b>을 획득해보세요! ✨
        </p>
    </div>
""", unsafe_allow_html=True)

# 5. MBTI 간이 진단 기기
with st.expander("🤔 내 MBTI를 모르겠다면? 3초 간이 테스트"):
    st.write("알맞은 행동 양식을 골라주시면 MBTI가 조합됩니다.")
    q1 = st.radio("1. 에너지를 어디서 충전하나요?", ["친구들과 활기차게 어울리기 (E)", "집에서 조용히 혼자 시간 보내기 (I)"])
    q2 = st.radio("2. 평소 생각을 구상할 때?", ["눈앞의 팩트와 생생한 현실에 집중 (S)", "머릿속 상상과 미래의 가능성에 무게 (N)"])
    q3 = st.radio("3. 타인을 위로하는 방식은?", ["상황 분석 및 이성적인 피드백 (T)", "속상한 마음에 격하게 감정 공감하기 (F)"])
    q4 = st.radio("4. 과제를 할 때 스타일은?", ["체계적인 시간 계획 및 실천 (J)", "직전까지 미루다 벼락치기로 돌파 (P)"])
    
    calc_mbti = (
        ("E" if "E" in q1 else "I") +
        ("S" if "S" in q2 else "N") +
        ("T" if "T" in q3 else "F") +
        ("J" if "J" in q4 else "P")
    )
    st.success(f"나의 매칭 MBTI: **{calc_mbti}**")
    if st.button("계산된 MBTI 적용하기 🎯"):
        st.session_state["mbti_val"] = calc_mbti
        st.toast(f"{calc_mbti}가 적용되었습니다!")

# 6. 메인 입력창 연동
mbti_list = sorted(list(mbti_pokemon.keys()))
default_mbti = st.session_state.get("mbti_val", "ENFP")

col_sel = st.columns([1, 2, 1])
with col_sel[1]:
    selected_mbti = st.selectbox("👇 당신의 진짜 MBTI는 무엇인가요?", mbti_list, index=mbti_list.index(default_mbti))

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# 7. 포켓볼 소환 액션
if st.button("🔴 포켓볼 던져서 소환하기! 🔴", use_container_width=True):
    
    # 7-1. 귀여운 가짜 대기 시간
    with st.spinner('포켓볼이 마구 흔들립니다... 덜컹! 덜컹!'):
        time.sleep(1.2)
        
    pokemon = mbti_pokemon[selected_mbti]
    partner_mbti = pokemon["partner"]
    partner_pokemon = mbti_pokemon[partner_mbti]
    
    # 7-2. ★★ 10% 이로치 가챠 시스템 구현 ★★
    # random.random()은 0.0과 1.0 사이의 실수를 임의로 반환합니다.
    # 0.1보다 작을 확률이 정확히 10%입니다!
    is_shiny = random.random() < 0.10
    
    # 7-3. ★★ 움직이는 쇼다운 gif 연동 ★★
    # PokeAPI의 showdown 서브 에셋 폴더에 들어있는 움직이는 gif 주소입니다.
    if is_shiny:
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/shiny/{pokemon['id']}.gif"
        st.balloons() # 이로치 전용 축하 팡팡 효과
        st.toast("🚨 대박! 10%의 행운! 초희귀 이로치 포켓몬 당첨! 🚨")
    else:
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{pokemon['id']}.gif"
        st.snow() # 일반 소환 시 아늑하게 눈 내리는 효과
    
    # 7-4. 울음소리 자동 재생 주입
    cry_url = f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{pokemon['id']}.ogg"
    st.markdown(f'<audio src="{cry_url}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
    
    # 7-5. 소환 결과 텍스트 안내
    if is_shiny:
        st.warning(f"✨ 축하합니다! 반짝이는 이로치 {pokemon['name']}(이)가 소환되었습니다!")
    else:
        st.success(f"🎉 성공! 귀여운 {pokemon['name']}(이)가 무사히 소환되었습니다!")

    # 8. 애니메이션 포켓몬 전용 아기자기한 카드 레이아웃
    card_class = "shiny-card" if is_shiny else "result-card"
    st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 1.2])
    
    with c1:
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        # 움직이는 포켓몬 배치 (픽셀 아트가 찌그러지지 않게 150px 고정 크기 제공)
        st.image(image_url, caption="움직이는 실제 모습 👾", width=150)
        
        if is_shiny:
            st.markdown("<p style='text-align:center; color:#E63946; font-weight:bold; font-size:1.1em;'>✨ SHINY! ✨</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='text-align:center; color:#6C757D; font-size:0.9em;'>도감 NO. {pokemon['id']}</p>", unsafe_allow_html=True)
            
    with c2:
        st.markdown(f"### {pokemon['emoji']} {pokemon['name']}")
        st.markdown(f"<span class='pokemon-type'>타입: {pokemon['type']}</span>", unsafe_allow_html=True)
        st.write(pokemon['desc'])
        
        # 성격 능력치 스탯 바 표시
        st.markdown("<p style='margin-bottom:2px; font-weight:bold; font-size:0.95em;'>🎮 종족 능력치 분석</p>", unsafe_allow_html=True)
        for stat_name, stat_val in pokemon["stats"].items():
            # 150 기준 백분율로 채움
            normalized_val = min(1.0, stat_val / 150.0)
            col_st1, col_st2 = st.columns([1.5, 3.5])
            with col_st1:
                st.markdown(f"<span class='stat-label'>{stat_name}: {stat_val}</span>", unsafe_allow_html=True)
            with col_st2:
                # 스탯에 따라 예쁜 파스텔 바 색칠하기
                st.progress(normalized_val)
                
        # 환상의 궁합
        st.markdown(f"""
            <div class='partner-box'>
                🤝 <b>최강의 소울메이트:</b> {partner_mbti} ({partner_pokemon['name']})<br>
                <small>함께 공부하거나 협동 게임을 할 때 최고의 파트너십을 보여줍니다!</small>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
    st.info(f"💡 **10% 가챠 도전!** 과연 한 번에 이로치 포켓몬을 뽑은 금손 친구는 누구일까요? 링크를 공유해 대결해 보세요! 🏆")

# 9. 푸터 영역
st.markdown("""
    <div class="footer">
        💖 제작: 당곡고등학교 멋쟁이 개발자 학생 🎓 | Powered by Streamlit & PokeAPI Showdown GIF
    </div>
""", unsafe_allow_html=True)
