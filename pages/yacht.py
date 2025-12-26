import random
from collections import Counter

import streamlit as st

CATEGORIES = [
    "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes", "Choice", "Four of a Kind", "Full House", "Small Straight", "Large Straight", "Yatch"
]

def score_category(dice: list[int], cat: str) -> int:
    cnt = Counter(dice)
    total = sum(dice)
    uniq = sorted(set(dice))

    if cat in {"Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"}:
        face = {"Ones":1, "Twos":2, "Threes":3, "Fours":4, "Fives":5, "Sixes":6}[cat]
        return face * cnt[face]
    
    if cat == "Choice":
        return total
    
    if cat == "Four of a Kind":
        return total if any(v >= 4 for v in cnt.values()) else 0
    
    if cat == "Full House":
        return total if sorted(cnt.values()) == [2, 3] else 0
    
    if cat == "Small Straight":
        straight = [{1,2,3,4}, {2,3,4,5}, {3,4,5,6}]
        s = set(dice)
        return 15 if any(straight.issubset(s) for straight in straight) else 0
    
    if cat == "Large Straight":
        s = set(dice)
        return 30 if s == {1,2,3,4,5} or s == {2,3,4,5,6} else 0
    
    if cat == "Yatch":
        return 50 if len(cnt) == 1 else 0
    
    return 0

# Helper
def init_state():
    if "y_dice" not in st.session_state:
        st.session_state.y_dice = [random.randint(1, 6) for  _ in range(5)]
    if "y_hold" not in st.session_state:
        st.session_state.y_hold = [False] * 5
    if "y_rolls_left" not in st.session_state:
        st.session_state.y_rolls_left = 3
    if "y_scores" not in st.session_state:
        st.session_state.y_scores = {c: None for c in CATEGORIES}
    if "y_message" not in st.session_state:
        st.session_state.y_message = ""

def reset_turn(keep_scores: bool = True):
    st.session_state.y_dice = [random.randint(1, 6) for _ in range(5)]
    st.session_state.y_hole = [False] * 5
    st.session_state.y_rolls_left = 3
    st.session_state.y_message = "" if keep_scores else st.session_state.y_message

def reset_game():
    st.session_state.y_scores = {c: None for c in CATEGORIES}
    reset_turn(keep_scores=False)
    st.session_state.y_message = "NEW GAME"

def roll_dice():
    if st.session_state.y_rolls_left <= 0:
        st.session_state.y_message = "이번턴은 더이상 굴릴수 없습니다. 카테고리를 선택하세요."
        return
    for i in range(5):
        if not st.session_state.y_hold[i]:
            st.session_state.y_dice[i] = random.randint(1, 6)
    st.session_state.y_rolls_left -= 1
    st.session_state.y_message = f"굴림 완료. 남은 굴림: {st.session_state.y_rolls_left}"

def total_score() -> int:
    return sum(v for  v in st.session_state.y_scores.values() if isinstance(v, int))

def is_game_over() -> bool:
    return all(v is not None for v in st.session_state.y_scores.values())

# UI
st.set_page_config(page_title="Yacht", layout="centered")
st.title("Yacht (1인용)")

init_state()

# control
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("굴리기", use_container_width=True):
        roll_dice()

with c2:
    if st.button("턴 리셋(점수유지)", use_container_width=True):
        reset_turn(keep_scores=True)

with c3:
    if st.button("새 게임(전체 초기화)", use_container_width=True):
        reset_game()

msg = st.session_state.get("y_message", "")
if msg:
    st.info(msg)

st.subheader("주사위")
dice_cols = st.columns(5)
for i, col in enumerate(dice_cols):
    with col:
        st.markdown(F"### {st.session_state.y_dice[i]}")
        st.session_state.y_hold[i] = st.checkbox(
            "홀드", value=st.session_state.y_hold[i], key=f"y_hold_{i}"
        )

st.caption(f"남은 굴림: {st.session_state.y_rolls_left} (턴당 최대 3회)")

st.divider()

st.subheader("점수판")
st.write(f"현재 합계: **{total_score()}**")

# score
for cat in CATEGORIES:
    chosen = st.session_state.y_scores[cat] is not None 
    pts = score_category(st.session_state.y_dice, cat)

    row = st.columns([2.5, 1.2, 1.3])
    with row[0]:
        st.write(f"**{cat}**" + (" (확정)" if chosen else ""))
    with row[1]:
        st.write(f"{st.session_state.y_scores[cat] if chosen else pts}")
    with row[2]:
        if chosen:
            st.button("선택됨", disabled=True, key=f"y_btn_{cat}")
        else:
            if st.button("선택", key=f"y_btn_{cat}"):
                st.session_state.y_scores[cat] = pts

                reset_turn(keep_scores=True)
                st.session_state.y_message = f"{cat}에 **{pts}점**을 기록했습니다."

st.divider()

if is_game_over():
    st.success(f"게임 종료. 최종점수: **{total_score()}**")
    st.write("원하시면 `초기화`로 다시 시작하세요.")
else:
    remaining = sum(1 for v in st.session_state.y_scores.values() if v is None)
    st.caption(f"남은 카테고리: {remaining}개")
