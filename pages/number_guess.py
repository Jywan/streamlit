import random
import streamlit as st


st.set_page_config(page_title="숫자 맞추기", layout="centered")

st.title("숫자 맞추기 게임")
st.caption("1~100 사이 숫자를 맞춰보세요.")

def reset_game():
    st.session_state.ng_answer = random.randint(1, 100)
    st.session_state.ng_tries = 0
    st.session_state.ng_history = []

# 페이지별 상태 키를 고유하게(ng_*) 사용
if "ng_answer" not in st.session_state:
    reset_game()
if "ng_tries" not in st.session_state:
    st.session_state.ng_tries = 0
if "ng_history" not in st.session_state:
    st.session_state.ng_history = []

guess = st.number_input("추측한 숫자", min_value=1, max_value=100, step=1)

col1, col2 = st.columns(2)
with col1:
    if st.button("제출", use_container_width=True):
        st.session_state.ng_tries += 1
        st.session_state.ng_history.append(int(guess))

        if guess < st.session_state.ng_answer:
            st.warning("업(UP) — 더 큰 숫자입니다.")
        elif guess > st.session_state.ng_answer:
            st.warning("다운(DOWN) — 더 작은 숫자입니다.")
        else:
            st.success(f"정답입니다. 시도 횟수: {st.session_state.ng_tries}")

with col2:
    if st.button("새 게임", use_container_width=True):
        reset_game()
        st.info("게임이 초기화되었습니다.")

st.divider()
st.write("시도 기록:", st.session_state.ng_history)