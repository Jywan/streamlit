import streamlit as st

from src.yacht.domain import CATEGORIES, score_category, total_score, is_game_over
from src.yacht.state import init_state, roll_dice, reset_game, reset_turn
from src.yacht.dice_ui import render_real_dice

st.set_page_config(page_title="Yacht", layout="centered")
st.title("Yacht (1인용)")

init_state()

# 컨트롤
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("굴리기", use_container_width=True):
        roll_dice()
with c2:
    if st.button("턴 리셋(점수 유지)", use_container_width=True):
        reset_turn(keep_message=True)
with c3:
    if st.button("새 게임(전체 초기화)", use_container_width=True):
        reset_game()

msg = st.session_state.get("y_message", "")
if msg:
    st.info(msg)

# area
st.subheader("주사위")
render_real_dice(st.session_state.y_dice, st.session_state.y_hold, st.session_state.y_roll_id)

hold_cols = st.columns(5)
for i, col in enumerate(hold_cols):
    with col:
        st.session_state.y_hold[i] = st.checkbox(
            "홀드", value=st.session_state.y_hold[i], key=f"y_hold_{i}"
        )

st.caption(f"남은 굴림: {st.session_state.y_rolls_left} (턴당 최대 3회)")

st.divider()
st.subheader("점수판")
st.write(f"현재 합계: **{total_score(st.session_state.y_scores)}**")

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
                reset_turn(keep_message=True)
                st.session_state.y_message = f"{cat}에 **{pts}점**을 기록했습니다."

st.divider()

if is_game_over(st.session_state.y_scores):
    st.success(f"게임 종료. 최종점수: **{total_score(st.session_state.y_scores)}**")
else:
    remaining = sum(1 for v in st.session_state.y_scores.values() if v is None)
    st.caption(f"남은 카테고리: {remaining}개")