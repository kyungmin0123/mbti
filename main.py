import streamlit as st
import time
import random

# 1. 페이지 초기 설정
st.set_page_config(
    page_title="포켓몬 MBTI 수집형 RPG 🎮",
    page_icon="🎒",
    layout="centered"
)

# 2. 게임 상태(State) 저장을 위한 세션 관리 선언
if "stage" not in st.session_state:
    st.session_state.stage = "summon"  # summon -> lobby -> battle -> victory/defeat
# 내가 수집한 포켓몬 목록 (도감)
if "my_collection" not in st.session_state:
    st.session_state.my_collection = []
# 현재 선택된 활성 파트너 포켓몬의 인덱스
if "active_index" not in st.session_state:
    st.session_state.active_index = 0

# 배틀용 임시 세션들
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
if "skill_cooldown" not in st.session_state:
    st.session_state.skill_cooldown = 0

# 3. 게임 테마 CSS 스타일 적용
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp {
        background: linear-gradient(135deg, #FFF0F5 0%, #E6F8FF 50%, #F3E8FF 100%) !important;
        background-attachment: fixed;
    }
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
    .console-box {
        background-color: #0f172a;
        border: 3px solid #334155;
        border-radius: 12px;
        padding: 15px;
        height: 200px;
        overflow-y: auto;
        font-family: 'Courier New', Courier, monospace;
        color: #38bdf8;
        font-size: 0.9em;
        line-height: 1.6;
    }
    .lobby-card {
        background: rgba(255, 255, 255, 0.9);
        border: 4px solid #FFCB05;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        color: #2D3748;
    }
    .stat-text {
        font-weight: bold;
        color: #2D3748;
    }
    </style>
""", unsafe_allow_html=True)

# 4. MBTI 포켓몬 도감 데이터 기본 정의
mbti_pokemon_data = {
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

# 야생 출현용 보스 목록
boss_pool = [
    {"name": "뮤츠", "id": 150, "type": "에스퍼", "hp": 110, "atk": 110, "df": 90, "spd": 130, "emoji": "🔮", "desc": "연구소의 유전자 변형으로 태어난 궁극의 전설 포켓몬!"},
    {"name": "한카리아스", "id": 445, "type": "드래곤 / 땅", "hp": 108, "atk": 130, "df": 95, "spd": 102, "emoji": "🦈", "desc": "제트기 같은 무시무시한 스피드로 사냥감을 포획하는 사막의 지배자!"},
    {"name": "그란돈", "id": 383, "type": "땅", "hp": 100, "atk": 150, "df": 140, "spd": 90, "emoji": "🌋", "desc": "대지를 넓히고 용암을 제어하는 고대의 초전설 포켓몬!"},
    {"name": "가이오가", "id": 382, "type": "물", "hp": 100, "atk": 100, "df": 90, "spd": 90, "emoji": "🐋", "desc": "바다를 넓히고 폭우를 부르는 심해의 초전설 포켓몬!"}
]

# 5. 전용 체력바 그리기 함수
def render_hp_bar(current, max_val, name, is_enemy=False):
    percent = int((current / max_val) * 100) if max_val > 0 else 0
    bar_color = "#10B981" if percent > 50 else "#FBBF24" if percent > 20 else "#EF4444"
    align = "right" if is_enemy else "left"
    st.markdown(f"""
        <div style="text-align: {align}; margin-bottom: 5px;">
            <b style="color: #fff; font-size: 1.05em;">{name}</b>
        </div>
        <div style="background-color: #2d3748; border: 2px solid #4a5568; border-radius: 8px; height: 18px; width: 100%; overflow: hidden; position: relative; margin-bottom: 12px;">
            <div style="background-color: {bar_color}; width: {percent}%; height: 100%; transition: width 0.3s;"></div>
            <div style="position: absolute; width: 100%; text-align: center; top: 0; left: 0; font-size: 11px; color: white; font-weight: bold; line-height: 15px;">
                HP: {current} / {max_val} ({percent}%)
            </div>
        </div>
    """, unsafe_allow_html=True)

# 6. 배틀 매커니즘 초기화 함수
def init_battle():
    boss = random.choice(boss_pool)
    boss_shiny = random.random() < 0.10 # 10% 확률로 이로치 보스 등장
    
    st.session_state.enemy_pokemon = {
        "name": boss["name"],
        "id": boss["id"],
        "type": boss["type"],
        "stats": {"HP": boss["hp"], "공격": boss["atk"], "방어": boss["df"], "스피드": boss["spd"]},
        "is_shiny": boss_shiny,
        "emoji": boss["emoji"],
        "desc": boss["desc"]
    }
    
    # 내 현재 포켓몬 정보 불러오기
    my_poke = st.session_state.my_collection[st.session_state.active_index]
    lvl_scale = 1.0 + (my_poke["level"] - 1) * 0.1
    
    # 밸런스를 위한 HP 스케일 가공
    p_hp = int(my_poke["stats"]["HP"] * lvl_scale * 2)
    e_hp = int(boss["hp"] * 1.5)
    
    st.session_state.player_hp = p_hp
    st.session_state.max_player_hp = p_hp
    st.session_state.enemy_hp = e_hp
    st.session_state.max_enemy_hp = e_hp
    
    # 오디오 재생 (보스 출현)
    boss_cry_url = f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{boss['id']}.ogg"
    st.markdown(f'<audio src="{boss_cry_url}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
    
    st.session_state.battle_log = [f"💥 크아아앙! 야생의 보스 '{boss['name']}'(이)가 울부짖으며 등장했습니다!"]
    st.session_state.skill_cooldown = 0
    st.session_state.stage = "battle"

# 7. ★★ 스피드(Speed) 기반 턴바이턴 배틀 연산 ★★
def resolve_turn(player_action):
    my_poke = st.session_state.my_collection[st.session_state.active_index]
    lvl_scale = 1.0 + (my_poke["level"] - 1) * 0.1
    
    # 능력치 산출
    p_atk = int(my_poke["stats"]["공격"] * lvl_scale)
    p_def = int(my_poke["stats"]["방어"] * lvl_scale)
    p_spd = int(my_poke["stats"]["스피드"] * lvl_scale)
    
    e_poke = st.session_state.enemy_pokemon
    e_atk = e_poke["stats"]["공격"]
    e_def = e_poke["stats"]["방어"]
    e_spd = e_poke["stats"]["스피드"]
    
    # 적 AI 행동 결정 (80% 공격, 20% 방어)
    enemy_action = "attack" if random.random() < 0.80 else "defend"
    
    # 턴 행동 기록 헬퍼 함수
    def do_player_action():
        if player_action == "attack":
            dmg = max(10, int(p_atk * 0.5 - e_def * 0.2 + random.randint(-4, 4)))
            if enemy_action == "defend":
                dmg = max(3, int(dmg * 0.3))
                st.session_state.battle_log.append(f"🛡️ 야생의 {e_poke['name']}가 방어하여 공격을 경감했습니다!")
            st.session_state.enemy_hp = max(0, st.session_state.enemy_hp - dmg)
            st.session_state.battle_log.append(f"⚔️ {my_poke['name']}의 몸통박치기! {e_poke['name']}에게 {dmg}의 대미지!")
        elif player_action == "special":
            dmg = max(25, int(p_atk * 1.15 - e_def * 0.2 + random.randint(5, 12)))
            if enemy_action == "defend":
                dmg = max(8, int(dmg * 0.4))
            st.session_state.enemy_hp = max(0, st.session_state.enemy_hp - dmg)
            st.session_state.battle_log.append(f"🔥 {my_poke['name']}의 MBTI 전용 일격!! {e_poke['name']}에게 {dmg}의 파괴적인 대미지!")
            st.session_state.skill_cooldown = 3
        elif player_action == "defend":
            st.session_state.battle_log.append(f"🛡️ {my_poke['name']}가 단단해지기를 사용해 단단히 대비합니다!")
            
    def do_enemy_action():
        if enemy_action == "attack":
            dmg = max(8, int(e_atk * 0.45 - p_def * 0.2 + random.randint(-3, 3)))
            if player_action == "defend":
                dmg = max(2, int(dmg * 0.3))
                st.session_state.battle_log.append(f"🛡️ {my_poke['name']}의 완벽한 가드! 대미지가 크게 감소합니다.")
            st.session_state.player_hp = max(0, st.session_state.player_hp - dmg)
            st.session_state.battle_log.append(f"⚡ {e_poke['name']}의 휘두르기! {my_poke['name']}에게 {dmg}의 대미지!")
        elif enemy_action == "defend":
            st.session_state.battle_log.append(f"🛡️ {e_poke['name']}가 방어 자세를 취해 몸을 웅크렸습니다.")

    # 쿨다운 차감
    if st.session_state.skill_cooldown > 0:
        st.session_state.skill_cooldown -= 1

    # 스피드 비교에 따른 실제 동작 제어 (진짜 턴제!)
    if p_spd >= e_spd:
        st.session_state.battle_log.append(f"💨 {my_poke['name']}(스피드 {p_spd})이(가) 더 빨라 선제 공격 기회를 잡았습니다!")
        # 1. 아군 공격
        do_player_action()
        # 상대 기절 체크
        if st.session_state.enemy_hp <= 0:
            st.session_state.battle_log.append(f"🏆 {e_poke['name']}이(가) 쓰러졌습니다!")
            st.session_state.stage = "victory"
            apply_victory_rewards()
            return
        # 2. 적군 공격
        do_enemy_action()
    else:
        st.session_state.battle_log.append(f"⚠️ {e_poke['name']}(스피드 {e_spd})이(가) 더 빨라 먼저 행동을 개시했습니다!")
        # 1. 적군 공격
        do_enemy_action()
        # 아군 기절 체크
        if st.session_state.player_hp <= 0:
            st.session_state.battle_log.append(f"💀 {my_poke['name']}가 패배하여 시야가 캄캄해졌습니다...")
            st.session_state.stage = "defeat"
            return
        # 2. 아군 공격
        do_player_action()
        # 상대 기절 체크
        if st.session_state.enemy_hp <= 0:
            st.session_state.battle_log.append(f"🏆 {e_poke['name']}이(가) 쓰러졌습니다!")
            st.session_state.stage = "victory"
            apply_victory_rewards()
            return

    # 라운드 종료 후 아군 패배 최종 체크 (동시에 쓰러졌거나 후공 패배 처리)
    if st.session_state.player_hp <= 0:
        st.session_state.battle_log.append(f"💀 {my_poke['name']}가 쓰러져 눈앞이 흐려집니다...")
        st.session_state.stage = "defeat"

# 8. 배틀 승리 보상 정산
def apply_victory_rewards():
    my_poke = st.session_state.my_collection[st.session_state.active_index]
    exp_gain = 50
    my_poke["exp"] += exp_gain
    st.session_state.battle_log.append(f"⭐ 파트너 {my_poke['name']}가 경험치 {exp_gain}을 얻었습니다.")
    
    # 레벨업 체크
    if my_poke["exp"] >= 100:
        my_poke["level"] += 1
        my_poke["exp"] = my_poke["exp"] % 100
        st.session_state.battle_log.append(f"🎉 LEVEL UP! {my_poke['name']}의 레벨이 {my_poke['level']}(으)로 상승했습니다! 능력치가 10% 강해집니다.")

# ----------------- UI 및 분기 제어 -----------------

st.markdown("<h1 class='game-title'>👾 POKÉMON MBTI RPG 👾</h1>", unsafe_allow_html=True)
st.write("---")

# [1] 스타터 생성 스테이지 (10% 확률 리얼 이로치 구현)
if st.session_state.stage == "summon":
    st.markdown("""
        <div class="lobby-card">
            <h3 style="margin-top:0;">🎒 1단계: 내 MBTI로 스타터 포켓몬 생성</h3>
            <p>당신의 성격 유형을 입력하세요. 운명처럼 매칭되는 귀여운 파트너가 소환됩니다!<br>
            소환 시 <b>정확히 10%의 연산 확률</b>로 은하수빛 찬란한 <b>이로치(Shiny)</b>가 탄생합니다!</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    mbti_list = sorted(list(mbti_pokemon_data.keys()))
    selected_mbti = st.selectbox("👇 당신의 성격을 나타내는 MBTI를 선택해 주세요!", mbti_list, index=0)
    
    if st.button("☄️ 몬스터볼 던지기!!", use_container_width=True):
        # 10% 확률 이로치 연산
        is_shiny = random.random() < 0.10
        base_pokemon = mbti_pokemon_data[selected_mbti]
        
        # 포켓몬 개별 딕셔너리 생성 (개별 성장 구현 목적)
        starter = {
            "name": base_pokemon["name"],
            "id": base_pokemon["id"],
            "emoji": base_pokemon["emoji"],
            "type": base_pokemon["type"],
            "stats": base_pokemon["stats"].copy(),
            "desc": base_pokemon["desc"],
            "is_shiny": is_shiny,
            "level": 1,
            "exp": 0
        }
        
        # 보관함에 주입
        st.session_state.my_collection = [starter]
        st.session_state.active_index = 0
        
        # 울음소리 자동 로드
        cry_url = f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{starter['id']}.ogg"
        st.markdown(f'<audio src="{cry_url}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)
        
        with st.spinner("운명의 포켓몬과 교감하는 중... ✨"):
            time.sleep(1.2)
            
        if is_shiny:
            st.balloons()
            st.warning(f"✨ 축하합니다! 10%의 행운! 아주 희귀한 [이로치 {starter['name']}]을(를) 맞이했습니다! ✨")
        else:
            st.snow()
            st.success(f"🎉 성공! 든든한 파트너 [{starter['name']}]와(과) 모험을 떠날 준비를 마쳤습니다!")
            
        st.session_state.stage = "lobby"
        st.rerun()

# [2] 캠프 및 보관함 관리 스테이지
elif st.session_state.stage == "lobby":
    st.markdown("### 🏕️ 포켓몬 캠프 및 보관함")
    
    # 2-1. 현재 활성 파트너 포켓몬 정보 띄우기
    active_poke = st.session_state.my_collection[st.session_state.active_index]
    lvl_scale = 1.0 + (active_poke["level"] - 1) * 0.1
    
    if active_poke["is_shiny"]:
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/shiny/{active_poke['id']}.gif"
        p_display_name = f"✨ 이로치 {active_poke['name']}"
    else:
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{active_poke['id']}.gif"
        p_display_name = active_poke["name"]
        
    col_l1, col_l2 = st.columns([1, 1.2])
    with col_l1:
        st.markdown("<div style='background: white; border-radius:15px; padding:15px; text-align:center;'>", unsafe_allow_html=True)
        st.image(sprite_url, width=130)
        st.markdown(f"<h4>{active_poke['emoji']} {p_display_name}</h4>", unsafe_allow_html=True)
        st.markdown(f"<span style='background-color:#4EA8DE; color:#fff; padding:3px 10px; border-radius:12px; font-size:0.8em;'>{active_poke['type']}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_l2:
        st.markdown("<div class='lobby-card'>", unsafe_allow_html=True)
        st.markdown(f"<h4>📊 {p_display_name} 상세 스펙</h4>", unsafe_allow_html=True)
        st.write(f"🌟 **레벨:** Lv. {active_poke['level']}")
        st.write(f"⭐ **경험치:** {active_poke['exp']} / 100")
        st.progress(active_poke['exp'] / 100)
        st.write("---")
        st.write(f"❤️ **체력(HP):** {int(active_poke['stats']['HP'] * lvl_scale * 2)}")
        st.write(f"⚔️ **공격력:** {int(active_poke['stats']['공격'] * lvl_scale)} (기본: {active_poke['stats']['공격']})")
        st.write(f"🛡️ **방어력:** {int(active_poke['stats']['방어'] * lvl_scale)} (기본: {active_poke['stats']['방어']})")
        st.write(f"⚡ **스피드:** {int(active_poke['stats']['스피드'] * lvl_scale)} (기본: {active_poke['stats']['스피드']})")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("---")
    
    # 2-2. ★★ 주머니 보관함 및 선택 교체 UI ★★
    st.markdown("<h4>🎒 나의 포켓몬 보관함 (가방)</h4>", unsafe_allow_html=True)
    poke_names = []
    for idx, p in enumerate(st.session_state.my_collection):
        shiny_tag = "✨ 이로치 " if p["is_shiny"] else ""
        poke_names.append(f"{idx+1}. {shiny_tag}{p['name']} (Lv.{p['level']})")
        
    # 가방에서 전투에 내보낼 활성 포켓몬 바꾸기
    selected_idx = st.selectbox("출격시킬 포켓몬 파트너를 선택하세요:", range(len(st.session_state.my_collection)), format_func=lambda x: poke_names[x])
    if selected_idx != st.session_state.active_index:
        st.session_state.active_index = selected_idx
        st.toast(f"출전 포켓몬을 변경했습니다!")
        st.rerun()
        
    st.write("---")
    
    # 모험 나가기 버튼들
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("🌳 풀숲으로 들어가 모험하기 (배틀 개시)", use_container_width=True):
            init_battle()
            st.rerun()
    with col_nav2:
        if st.button("🔄 전체 초기화 후 처음부터 시작하기", use_container_width=True):
            st.session_state.stage = "summon"
            st.session_state.my_collection = []
            st.session_state.active_index = 0
            st.rerun()

# [3] 턴제 배틀 격투판 스테이지
elif st.session_state.stage == "battle":
    p_poke = st.session_state.my_collection[st.session_state.active_index]
    e_poke = st.session_state.enemy_pokemon
    
    if p_poke["is_shiny"]:
        p_sprite = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/shiny/{p_poke['id']}.gif"
    else:
        p_sprite = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{p_poke['id']}.gif"
        
    if e_poke["is_shiny"]:
        e_sprite = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/shiny/{e_poke['id']}.gif"
    else:
        e_sprite = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{e_poke['id']}.gif"
        
    st.markdown("<div class='gameboy-panel'>", unsafe_allow_html=True)
    
    col_bat1, col_bat2 = st.columns(2)
    with col_bat1:
        render_hp_bar(st.session_state.player_hp, st.session_state.max_player_hp, f"Lv. {p_poke['level']} {p_poke['name']}")
        st.image(p_sprite, width=130)
        
    with col_bat2:
        render_hp_bar(st.session_state.enemy_hp, st.session_state.max_enemy_hp, f"⚠️ BOSS 야생의 {e_poke['name']}", is_enemy=True)
        col_align1, col_align2 = st.columns([1, 2])
        with col_align2:
            st.image(e_sprite, width=130)
            if e_poke["is_shiny"]:
                st.markdown("<p style='color:#FFDE00; font-weight:bold; font-size:0.9em; margin:0;'>✨ 희귀 이로치 보스!</p>", unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("💬 **턴 진행 텍스트 중계:**")
    reversed_logs = "<br>".join([f"• {log}" for log in reversed(st.session_state.battle_log)])
    st.markdown(f"<div class='console-box'>{reversed_logs}</div>", unsafe_allow_html=True)
    st.write("---")
    
    st.write("🎮 **명령어 조작 패널:**")
    cmd1, cmd2, cmd3 = st.columns(3)
    with cmd1:
        if st.button("⚔️ 몸통박치기 (일반)", use_container_width=True):
            resolve_turn("attack")
            st.rerun()
    with cmd2:
        if st.session_state.skill_cooldown == 0:
            if st.button("🔥 필살기 (쿨타임)", use_container_width=True):
                resolve_turn("special")
                st.rerun()
        else:
            st.button(f"⏳ 대기 ({st.session_state.skill_cooldown}턴)", disabled=True, use_container_width=True)
    with cmd3:
        if st.button("🛡️ 방어 (대미지 감소)", use_container_width=True):
            resolve_turn("defend")
            st.rerun()

# [4] 배틀 결과 및 수집 정산 스테이지
elif st.session_state.stage in ["victory", "defeat"]:
    e_poke = st.session_state.enemy_pokemon
    st.markdown("<div class='lobby-card' style='text-align:center;'>", unsafe_allow_html=True)
    
    if st.session_state.stage == "victory":
        st.balloons()
        st.markdown(f"<h2 style='color: #4CAF50;'>🏆 VICTORY - 배틀 승리! 🏆</h2>", unsafe_allow_html=True)
        st.write(f"야생의 강력한 {e_poke['name']}을(를) 완벽히 제압해 굴복시켰습니다!")
        
        st.write("---")
        # ★★ [새 기능] 이기면 상대 포켓몬 얻기 버튼 ★★
        st.markdown(f"🧬 **포획 분석 보고서:** {e_poke['desc']}")
        if st.button(f"🎒 {e_poke['name']}을(를) 내 가방에 수집하기 (포획!)", use_container_width=True):
            
            # 수집 목록에 들어갈 도감용 데이터 팩킹
            new_catch = {
                "name": e_poke["name"],
                "id": e_poke["id"],
                "emoji": e_poke["emoji"],
                "type": e_poke["type"],
                "stats": e_poke["stats"].copy(),
                "desc": e_poke["desc"],
                "is_shiny": e_poke["is_shiny"],
                "level": 1,
                "exp": 0
            }
            # 보관함에 주입
            st.session_state.my_collection.append(new_catch)
            st.toast(f"🎉 {e_poke['name']}이(가) 보관함에 추가되었습니다!")
            st.session_state.stage = "lobby"
            st.rerun()
            
    else:
        st.markdown("<h2 style='color: #F44336;'>💀 DEFEAT - 파트너 기절... 💀</h2>", unsafe_allow_html=True)
        st.write("눈앞이 캄캄해져 전선에서 퇴각했습니다. 포켓몬 센터에서 완전히 회복되었습니다.")
        
    st.write("---")
    st.write("💬 **전적 보고서 로그:**")
    reversed_logs = "<br>".join([f"• {log}" for log in reversed(st.session_state.battle_log)])
    st.markdown(f"<div class='console-box'>{reversed_logs}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    
    if st.button("🏕️ 안전하게 캠프로 귀환하기", use_container_width=True):
        st.session_state.stage = "lobby"
        st.rerun()

# 9. 푸터 크레딧
st.markdown("""
    <br><hr style='border: 0.5px solid #eaeaea;'>
    <div style="text-align: center; color: #8E9AAF; font-size: 0.85em;">
        🎒 당곡고등학교 게임 프로젝트 센터 🎓 | Powered by Streamlit Python Database
    </div>
""", unsafe_allow_html=True)
