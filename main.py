import streamlit as st
import time
import random

# 1. 페이지 초기 설정
st.set_page_config(
    page_title="포켓몬 MBTI 배틀 RPG 🎮",
    page_icon="⚔️",
    layout="centered"
)

# 2. 게임 상태(State) 저장을 위한 세션 관리 선언
if "stage" not in st.session_state:
    st.session_state.stage = "summon"  # summon(스타터선택) -> lobby(대기실) -> battle(배틀) -> result(승리/패배)
if "my_pokemon" not in st.session_state:
    st.session_state.my_pokemon = None
if "is_shiny_starter" not in st.session_state:
    st.session_state.is_shiny_starter = False
if "enemy_pokemon" not in st.session_state:
    st.session_state.enemy_pokemon = None
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 0
if "max_player_hp" not in st.session_state:
    st.session_state.max_player_hp = 0
if "enemy_hp" not in st.session_state:
    st.session_state.enemy_hp = 0
if "max_enemy_hp" not in st.session_state:
    st.session_state.max_enemy_hp = 0
if "battle_log" not in st.session_state:
    st.session_state.battle_log = []
if "my_level" not in st.session_state:
    st.session_state.my_level = 1
if "my_exp" not in st.session_state:
    st.session_state.my_exp = 0
if "skill_cooldown" not in st.session_state:
    st.session_state.skill_cooldown = 0

# 3. 게임 테마 전용 레트로 CSS 스타일 적용
st.markdown("""
    <style>
    /* 전체 배경: 사이버 픽셀 8비트 감성의 파스텔 블루 그라데이션 */
    [data-testid="stAppViewContainer"], .stApp {
        background: linear-gradient(135deg, #FFF0F5 0%, #E6F8FF 50%, #F3E8FF 100%) !important;
        background-attachment: fixed;
    }
    
    /* 게임보이 화면 스타일의 컨테이너 */
    .gameboy-panel {
        background-color: #1a1a2e;
        border: 5px solid #4a5568;
        border-radius: 20px;
        padding: 25px;
        box-shadow: inset 0 0 15px #000, 0 15px 30px rgba(0,0,0,0.3);
        color: #e2e8f0;
        margin-bottom: 20px;
    }
    
    .game-title {
        font-family: 'Courier New', monospace;
        font-size: 2.2em !important;
        font-weight: 900;
        text-align: center;
        color: #FFDE00;
        text-shadow: 2px 2px #FF0000, -2px -2px #000;
        margin-bottom: 5px;
    }
    
    /* 8비트 스타일 텍스트 콘솔 박스 (배틀로그용) */
    .console-box {
        background-color: #0f172a;
        border: 3px solid #334155;
        border-radius: 12px;
        padding: 15px;
        height: 180px;
        overflow-y: auto;
        font-family: 'Courier New', Courier, monospace;
        color: #38bdf8;
        font-size: 0.9em;
        line-height: 1.6;
    }
    
    /* 든든한 카드 상자 */
    .lobby-card {
        background: rgba(255, 255, 255, 0.9);
        border: 4px solid #FFCB05;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        color: #2D3748;
    }
    
    /* 타이포그래피 */
    .stat-text {
        font-weight: bold;
        color: #2D3748;
    }
    </style>
""", unsafe_allow_html=True)

# 4. MBTI 포켓몬 데이터 사전 정의 (공식 일러스트 ID 및 종족값 세팅)
mbti_pokemon = {
    "ISTJ": {"name": "이상해씨", "id": 1, "emoji": "🍃", "type": "풀 / 독", "partner": "ESFP", "stats": {"HP": 45, "공격": 49, "방어": 49, "스피드": 45}, "desc": "신중하고 성실한 계획의 대명사!"},
    "ISFJ": {"name": "메가니움", "id": 154, "emoji": "🌸", "type": "풀", "partner": "ESTP", "stats": {"HP": 80, "공격": 82, "방어": 100, "스피드": 80}, "desc": "헌신적이고 따뜻한 평화 수호자!"},
    "INFJ": {"name": "뮤", "id": 151, "emoji": "✨", "type": "에스퍼", "partner": "ENFP", "stats": {"HP": 100, "공격": 100, "방어": 100, "스피드": 100}, "desc": "신비롭고 맑은 신념을 지닌 영혼!"},
    "INTJ": {"name": "메타그로스", "id": 376, "emoji": "🤖", "type": "강철 / 에스퍼", "partner": "ENTP", "stats": {"HP": 80, "공격": 135, "방어": 130, "스피드": 70}, "desc": "완벽함을 추구하는 브레인 전략가!"},
    "ISTP": {"name": "개굴닌자", "id": 658, "emoji": "🐸", "type": "물 / 악", "partner": "ESFJ", "stats": {"HP": 72, "공격": 95, "방어": 67, "스피드": 122}, "desc": "말을 아끼며 상황을 타개하는 해결사!"},
    "ISFP": {"name": "이브이", "id": 133, "emoji": "🦊", "type": "노말", "partner": "ESTJ", "stats": {"HP": 55, "공격": 55, "방어": 50, "스피드": 55}, "desc": "무한한 발전 가능성을 지닌 예술가!"},
    "INFP": {"name": "푸린", "id": 39, "emoji": "🎈", "type": "노말 / 페어리", "partner": "ENFJ", "stats": {"HP": 115, "공격": 45, "방어": 20, "스피드": 20}, "desc": "낭만 가득하고 따뜻한 꿈을 가진 천사!"},
    "INTP": {"name": "로토무", "id": 479, "emoji": "⚡", "type": "전기 / 고스트", "partner": "ENTJ", "stats": {"HP": 50, "공격": 50, "방어": 77, "스피드": 91}, "desc": "호기심 많고 기계를 다루는 비평가!"},
    "ESTP": {"name": "윈디", "id": 59, "emoji": "🔥", "type": "불꽃", "partner": "ISFJ", "stats": {"HP": 90, "공격": 110, "방어": 80, "스피드": 95}, "desc": "활동적이며 위기를 스릴로 이기는 모험가!"},
    "ESFP": {"name": "토게피", "id": 175, "emoji": "🥚", "type": "페어리", "partner": "ISTJ", "stats": {"HP": 35, "공격": 20, "방어": 65, "스피드": 20}, "desc": "모두에게 긍정 바이러스를 퍼뜨리는 인싸!"},
    "ENFP": {"name": "피카츄", "id": 25, "emoji": "⚡️", "type": "전기", "partner": "INFJ", "stats": {"HP": 35, "공격": 55, "방어": 40, "스피드": 90}, "desc": "매력적인 성격으로 인기를 독차지하는 리더!"},
    "ENTP": {"name": "팬텀", "id": 94, "emoji": "😈", "type": "고스트 / 독", "partner": "INTJ", "stats": {"HP": 60, "공격": 65, "방어": 60, "스피드": 110}, "desc": "예상 밖의 재치와 위트가 흘러넘치는 유머러스!"},
    "ESTJ": {"name": "괴력몬", "id": 68, "emoji": "💪", "type": "격투", "partner": "ISFP", "stats": {"HP": 90, "공격": 130, "방어": 80, "스피드": 55}, "desc": "확실한 추진력으로 팀원들을 주도하는 장군!"},
    "ESFJ": {"name": "해피너스", "id": 242, "emoji": "💕", "type": "노말", "partner": "ISTP", "stats": {"HP": 255, "공격": 10, "방어": 10, "스피드": 55}, "desc": "치유의 에너지로 온 세상을 감싸는 평화 천사!"},
    "ENFJ": {"name": "망나뇽", "id": 149, "emoji": "🐉", "type": "드래곤 / 비행", "partner": "INFP", "stats": {"HP": 91, "공격": 134, "방어": 95, "스피드": 80}, "desc": "정의감과 따뜻한 리더십의 올바른 기준!"},
    "ENTJ": {"name": "리자몽", "id": 6, "emoji": "🔥", "type": "불꽃 / 비행", "partner": "INTP", "stats": {"HP": 78, "공격": 84, "방어": 78, "스피드": 100}, "desc": "과감하고 원대한 야망을 향해 날아가는 군주!"}
}

# 5. 전용 헬스 바 렌더링 헬퍼 함수 (진짜 게임보이 스타일 구현)
def render_hp_bar(current, max_val, name, is_enemy=False):
    percent = int((current / max_val) * 100) if max_val > 0 else 0
    # 체력 퍼센트에 따라 바 색상 동적 변경 (그린 -> 옐로우 -> 레드)
    if percent > 50:
        bar_color = "#10B981" # Green
    elif percent > 20:
        bar_color = "#FBBF24" # Yellow
    else:
        bar_color = "#EF4444" # Red
        
    align = "right" if is_enemy else "left"
    st.markdown(f"""
        <div style="text-align: {align}; margin-bottom: 5px;">
            <b style="color: #fff; font-size: 1.05em;">{name}</b>
        </div>
        <div style="background-color: #2d3748; border: 2px solid #4a5568; border-radius: 8px; height: 18px; width: 100%; overflow: hidden; position: relative; margin-bottom: 12px;">
            <div style="background-color: {bar_color}; width: {percent}%; height: 100%; transition: width 0.4s ease-in-out;"></div>
            <div style="position: absolute; width: 100%; text-align: center; top: 0; left: 0; font-size: 11px; color: white; font-weight: bold; line-height: 15px;">
                HP: {current} / {max_val} ({percent}%)
            </div>
        </div>
    """, unsafe_allow_html=True)

# 6. 배틀 세팅 및 매커니즘 도우미 함수들
def init_battle():
    # 6-1. 거대 야생 보스 목록
    boss_pool = [
        {"name": "뮤츠", "id": 150, "type": "에스퍼", "hp": 110, "atk": 110, "df": 90, "spd": 130},
        {"name": "한카리아스", "id": 445, "type": "드래곤 / 땅", "hp": 108, "atk": 130, "df": 95, "spd": 102},
        {"name": "레시라무", "id": 643, "type": "드래곤 / 불꽃", "hp": 100, "atk": 120, "df": 100, "spd": 90},
        {"name": "그란돈", "id": 383, "type": "땅", "hp": 100, "atk": 150, "df": 140, "spd": 90},
        {"name": "가이오가", "id": 382, "type": "물", "hp": 100, "atk": 100, "df": 90, "spd": 90}
    ]
    boss = random.choice(boss_pool)
    boss_shiny = random.random() < 0.10 # 보스 이로치 등장 10%
    
    st.session_state.enemy_pokemon = {
        "name": boss["name"],
        "id": boss["id"],
        "type": boss["type"],
        "stats": {"HP": boss["hp"], "공격": boss["atk"], "방어": boss["df"], "스피드": boss["spd"]},
        "is_shiny": boss_shiny
    }
    
    # 6-2. 스탯 레벨 스케일 반영 (내 레벨에 따라 스타터 체력/스탯 성장)
    lvl_scale = 1.0 + (st.session_state.my_level - 1) * 0.1
    p_hp = int(st.session_state.my_pokemon["stats"]["HP"] * lvl_scale * 2) # 배틀 연장을 위해 체력 상향 보정
    e_hp = int(boss["hp"] * 1.5)
    
    st.session_state.player_hp = p_hp
    st.session_state.max_player_hp = p_hp
    st.session_state.enemy_hp = e_hp
    st.session_state.max_enemy_hp = e_hp
    
    # 6-3. 오디오 재생 (보스 소환 소리!)
    boss_cry_url = f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{boss['id']}.ogg"
    st.markdown(f'<audio src="{boss_cry_url}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
    
    st.session_state.battle_log = [f"💥 크아아앙! 야생의 보스 '{boss['name']}'(이)가 울부짖으며 등장했습니다!"]
    st.session_state.skill_cooldown = 0
    st.session_state.stage = "battle"

def resolve_turn(action):
    # 내 능력치 계산 (레벨 증가 효과 영구 반영)
    lvl_scale = 1.0 + (st.session_state.my_level - 1) * 0.1
    p_atk = int(st.session_state.my_pokemon["stats"]["공격"] * lvl_scale)
    p_def = int(st.session_state.my_pokemon["stats"]["방어"] * lvl_scale)
    
    e_atk = st.session_state.enemy_pokemon["stats"]["공격"]
    e_def = st.session_state.enemy_pokemon["stats"]["방어"]
    
    # 1. 아군 턴 선제 행동
    p_damage = 0
    if action == "attack":
        p_damage = max(10, int(p_atk * 0.5 - e_def * 0.2 + random.randint(-4, 4)))
        st.session_state.enemy_hp = max(0, st.session_state.enemy_hp - p_damage)
        st.session_state.battle_log.append(f"⚔️ {st.session_state.my_pokemon['name']}의 기본 공격! {st.session_state.enemy_pokemon['name']}에게 {p_damage}의 피해!")
        if st.session_state.skill_cooldown > 0:
            st.session_state.skill_cooldown -= 1
            
    elif action == "special":
        p_damage = max(28, int(p_atk * 1.15 - e_def * 0.2 + random.randint(5, 12)))
        st.session_state.enemy_hp = max(0, st.session_state.enemy_hp - p_damage)
        st.session_state.battle_log.append(f"🔥 초강력 {st.session_state.my_pokemon['name']}의 MBTI 전용 필살기!! {st.session_state.enemy_pokemon['name']}에게 {p_damage}의 초월 피해를 가했습니다!!")
        st.session_state.skill_cooldown = 3 # 3턴 쿨타임
        
    elif action == "defend":
        st.session_state.battle_log.append(f"🛡️ {st.session_state.my_pokemon['name']}가 방어 태세를 취하여 다가올 피해를 극도로 낮춥니다!")
        if st.session_state.skill_cooldown > 0:
            st.session_state.skill_cooldown -= 1
            
    # 적의 쓰러짐 여부 체크
    if st.session_state.enemy_hp <= 0:
        st.session_state.battle_log.append(f"🏆 대성공! {st.session_state.enemy_pokemon['name']}을(를) 물리쳐 배틀에서 승리했습니다!")
        st.session_state.stage = "victory"
        
        # 보상 정산
        exp_earn = 50
        st.session_state.my_exp += exp_earn
        st.session_state.battle_log.append(f"⭐ 경험치(EXP) {exp_earn}을(를) 획득했습니다!")
        
        # 레벨 업 메커니즘
        if st.session_state.my_exp >= 100:
            st.session_state.my_level += 1
            st.session_state.my_exp = st.session_state.my_exp % 100
            st.session_state.battle_log.append(f"🎉 LEVEL UP!! 트레이너 레벨이 {st.session_state.my_level}(으)로 올랐습니다! 영구 공격/방어력이 10% 증가합니다!")
        return

    # 2. 적군 AI의 반격 턴
    e_damage = max(8, int(e_atk * 0.45 - p_def * 0.2 + random.randint(-3, 3)))
    if action == "defend":
        e_damage = max(2, int(e_damage * 0.3)) # 방어 시 대폭 경감
        
    st.session_state.player_hp = max(0, st.session_state.player_hp - e_damage)
    st.session_state.battle_log.append(f"⚡ {st.session_state.enemy_pokemon['name']}의 격렬한 공격! {st.session_state.my_pokemon['name']}는(은) {e_damage}의 피해를 입었습니다.")
    
    # 아군 쓰러짐 여부 체크
    if st.session_state.player_hp <= 0:
        st.session_state.battle_log.append(f"💀 아앗... {st.session_state.my_pokemon['name']}가 기절했습니다. 눈앞이 캄캄해집니다...")
        st.session_state.stage = "defeat"

# ----------------- UI 렌더링 -----------------

st.markdown("<h1 class='game-title'>👾 POKÉMON MBTI RPG 👾</h1>", unsafe_allow_html=True)
st.write("---")

# [STAGE 1] 스타터 포켓몬 소환 스크린 (10% 확률 이로치!)
if st.session_state.stage == "summon":
    st.markdown("""
        <div class="lobby-card">
            <h3 style="margin-top:0;">🎮 STEP 1: 나만의 MBTI 스타터 파트너 소환</h3>
            <p>당신의 성격 유형(MBTI)을 선택하면 운명의 스타터 포켓몬이 탄생합니다.<br>
            소환 시 <b>정확히 10% 확률</b>로 신비한 아우라를 가진 <b>이로치(Shiny)</b>가 탄생합니다! 도전해보세요!</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    mbti_list = sorted(list(mbti_pokemon.keys()))
    selected_mbti = st.selectbox("👇 당신의 MBTI를 알려주세요!", mbti_list, index=0)
    
    if st.button("☄️ 파트너 몬스터 볼 투척! (소환) ☄️", use_container_width=True):
        # 10%의 철저한 확률 가챠 연산
        is_shiny = random.random() < 0.10
        st.session_state.is_shiny_starter = is_shiny
        
        # 임시 보관
        st.session_state.my_pokemon = mbti_pokemon[selected_mbti]
        
        # 스타터 포켓몬 울음소리 재생
        cry_url = f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{st.session_state.my_pokemon['id']}.ogg"
        st.markdown(f'<audio src="{cry_url}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
        
        with st.spinner("야생의 파트너와 정신적으로 동조하는 중... ✨"):
            time.sleep(1.2)
            
        if is_shiny:
            st.balloons()
            st.warning("✨ 대박! 10%의 행운! 몸이 다르게 반짝이는 '이로치(Shiny)' 파트너를 소환했습니다! ✨")
        else:
            st.snow()
            st.success(f"🎉 동조 완료! 귀여운 파트너 {st.session_state.my_pokemon['name']}을(를) 얻었습니다!")
            
        st.session_state.stage = "lobby"
        st.rerun()

# [STAGE 2] 모험 로비 스크린 (스탯 확인, 전투 출격)
elif st.session_state.stage == "lobby":
    pokemon = st.session_state.my_pokemon
    is_shiny = st.session_state.is_shiny_starter
    
    # 쇽다운 GIF 주소 분기
    if is_shiny:
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/shiny/{pokemon['id']}.gif"
    else:
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{pokemon['id']}.gif"
        
    st.markdown("<h3 style='margin-bottom:5px;'>🏕️ 모험가 캠프 (Lobby)</h3>", unsafe_allow_html=True)
    
    col_l1, col_l2 = st.columns([1, 1.3])
    
    with col_l1:
        st.markdown("<div style='background: white; border-radius:15px; padding:15px; text-align:center;'>", unsafe_allow_html=True)
        st.image(sprite_url, width=140)
        st.markdown(f"<h4>{pokemon['emoji']} {pokemon['name'] if not is_shiny else '✨이로치 ' + pokemon['name']}</h4>", unsafe_allow_html=True)
        st.markdown(f"<span style='background-color:#EE1515; color:#fff; padding:3px 10px; border-radius:12px; font-size:0.8em;'>{pokemon['type']}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_l2:
        st.markdown("<div class='lobby-card'>", unsafe_allow_html=True)
        st.markdown(f"<h4>👑 트레이너 명함</h4>", unsafe_allow_html=True)
        st.write(f"🌟 **현재 레벨:** Lv. {st.session_state.my_level}")
        
        # 경험치바 (Streamlit 기본 progress 활용)
        st.write(f"⭐ **경험치 게이지:** {st.session_state.my_exp} / 100")
        st.progress(st.session_state.my_exp / 100)
        
        # 스탯 성장 시뮬레이션
        lvl_scale = 1.0 + (st.session_state.my_level - 1) * 0.1
        st.write("---")
        st.write("📈 **실제 전투 능력값 (레벨 상승치 반영됨):**")
        st.write(f"❤️ **체력(HP):** {int(pokemon['stats']['HP'] * lvl_scale * 2)}")
        st.write(f"⚔️ **공격력:** {int(pokemon['stats']['공격'] * lvl_scale)} (기본: {pokemon['stats']['공격']})")
        st.write(f"🛡️ **방어력:** {int(pokemon['stats']['방어'] * lvl_scale)} (기본: {pokemon['stats']['방어']})")
        st.write(f"⚡ **스피드:** {int(pokemon['stats']['스피드'] * lvl_scale)}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("---")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🌳 풀숲으로 들어가 야생 보스 찾기! (배틀)", use_container_width=True):
            init_battle()
            st.rerun()
    with col_btn2:
        if st.button("🔄 다른 MBTI 스타터로 다시 소환하기", use_container_width=True):
            st.session_state.stage = "summon"
            st.session_state.my_level = 1
            st.session_state.my_exp = 0
            st.rerun()

# [STAGE 3] 턴제 RPG 배틀 스크린 (실제 대결 구도)
elif st.session_state.stage == "battle":
    p_poke = st.session_state.my_pokemon
    e_poke = st.session_state.enemy_pokemon
    
    # 아군 GIF
    if st.session_state.is_shiny_starter:
        p_sprite = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/shiny/{p_poke['id']}.gif"
    else:
        p_sprite = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{p_poke['id']}.gif"
        
    # 보스 GIF
    if e_poke["is_shiny"]:
        e_sprite = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/shiny/{e_poke['id']}.gif"
    else:
        e_sprite = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{e_poke['id']}.gif"
        
    st.markdown("<div class='gameboy-panel'>", unsafe_allow_html=True)
    
    # 2컬럼 레이아웃 (좌: 나, 우: 야생보스)
    col_bat1, col_bat2 = st.columns(2)
    
    with col_bat1:
        render_hp_bar(st.session_state.player_hp, st.session_state.max_player_hp, f"Lv. {st.session_state.my_level} {p_poke['name']}")
        st.image(p_sprite, width=130)
        
    with col_bat2:
        render_hp_bar(st.session_state.enemy_hp, st.session_state.max_enemy_hp, f"⚠️ BOSS 야생의 {e_poke['name']}", is_enemy=True)
        # 보스가 우측에 있으므로 우측 정렬 느낌으로 배치
        col_align1, col_align2 = st.columns([1, 2])
        with col_align2:
            st.image(e_sprite, width=130)
            if e_poke["is_shiny"]:
                st.markdown("<p style='color:#FFDE00; font-weight:bold; font-size:0.9em; margin:0;'>✨ 희귀 보스 등장!</p>", unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 배틀 스크롤 로그 화면 출력 (Game 콘솔 느낌)
    st.write("💬 **배틀 상황 실시간 중계:**")
    # 로그를 뒤집어 최신 로그가 맨 위에 보이도록 설정
    reversed_logs = "<br>".join([f"• {log}" for log in reversed(st.session_state.battle_log)])
    st.markdown(f"<div class='console-box'>{reversed_logs}</div>", unsafe_allow_html=True)
    st.write("---")
    
    # 아군 조작 커맨드 버튼
    st.write("🎮 **명령을 선택하세요:**")
    cmd_col1, cmd_col2, cmd_col3 = st.columns(3)
    
    with cmd_col1:
        if st.button("⚔️ 몸통박치기 (일반공격)", use_container_width=True):
            resolve_turn("attack")
            st.rerun()
            
    with cmd_col2:
        # 쿨타임 여부에 따른 필살기 버튼 제어
        if st.session_state.skill_cooldown == 0:
            if st.button("🔥 MBTI 필살기! (강력)", use_container_width=True):
                resolve_turn("special")
                st.rerun()
        else:
            st.button(f"⏳ 필살기 쿨타임 ({st.session_state.skill_cooldown}턴 남음)", disabled=True, use_container_width=True)
            
    with cmd_col3:
        if st.button("🛡️ 방어 태세 (피해 최소화)", use_container_width=True):
            resolve_turn("defend")
            st.rerun()

# [STAGE 4] 배틀 결과 스크린 (승리 / 패배 축하 화면)
elif st.session_state.stage in ["victory", "defeat"]:
    st.markdown("<div class='lobby-card' style='text-align:center;'>", unsafe_allow_html=True)
    
    if st.session_state.stage == "victory":
        st.balloons()
        st.markdown("<h2 style='color: #4CAF50;'>🏆 VICTORY - 배틀에서 완승했습니다! 🏆</h2>", unsafe_allow_html=True)
        st.write(f"트레이너의 레벨 성장을 돕기 위해 보상이 지급되었습니다!")
    else:
        st.markdown("<h2 style='color: #F44336;'>💀 DEFEAT - 파트너가 쓰러졌습니다... 💀</h2>", unsafe_allow_html=True)
        st.write("걱정 마세요! 포켓몬 센터에서 완전히 회복되어 더 강한 모습으로 부활했습니다.")
        
    st.write("---")
    st.write("💬 **최종 전적 로그 기록:**")
    reversed_logs = "<br>".join([f"• {log}" for log in reversed(st.session_state.battle_log)])
    st.markdown(f"<div class='console-box'>{reversed_logs}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    
    if st.button("🏕️ 캠프로 무사히 돌아가기 (체력 완전 회복)", use_container_width=True):
        st.session_state.stage = "lobby"
        st.rerun()

# 10. 크레딧 푸터 영역
st.markdown("""
    <br><hr style='border: 0.5px solid #eaeaea;'>
    <div style="text-align: center; color: #8E9AAF; font-size: 0.85em;">
        🎮 당곡고등학교 게임 아카데미 🎓 | Powered by Streamlit Session State & Showdown Sprite API
    </div>
""", unsafe_allow_html=True)
