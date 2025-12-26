import random
import streamlit as st

st.set_page_config(page_title="가위바위보", layout="centered")

st.title("가위바위보")
st.caption("당신 vs 컴퓨터. 버튼 한 번으로 승부가 납니다.")

choices = ["가위", "바위", "보"]

def init_rps():
    if "rps_w" not in st.session_state: st.session_state.rps_w = 0
    if "rps_l" not in st.session_state: st.session_state.rps_l = 0
    if "rps_d" not in st.session_state: st.session_state.rps_d = 0
    if "rps_last" not in st.session_state: st.session_state.rps_last = None

init_rps()

c1, c2, c3 = st.columns(3)
user = None
with c1:
    if st.button("가위", use_container_width=True): user = "가위"
with c2:
    if st.button("바위", use_container_width=True): user = "바위"
with c3:
    if st.button("보", use_container_width=True): user = "보"

if user:
    cpu = random.choice(choices)

    # 승패 판정
    if user == cpu:
        result = "무승부"
        st.session_state.rps_d += 1
    elif (user, cpu) in [("가위", "보"), ("바위", "가위"), ("보", "바위")]:
        result = "승리"
        st.session_state.rps_w += 1
    else:
        result = "패배"
        st.session_state.rps_l += 1

    st.session_state.rps_last = (user, cpu, result)

st.divider()

if st.session_state.rps_last:
    u, c, r = st.session_state.rps_last
    st.write(f"당신: **{u}** / 컴퓨터: **{c}**")
    if r == "승리":
        st.success("결과: 승리")
    elif r == "패배":
        st.error("결과: 패배")
    else:
        st.info("결과: 무승부")

st.subheader("전적")
st.write(f"승 {st.session_state.rps_w} / 패 {st.session_state.rps_l} / 무 {st.session_state.rps_d}")

if st.button("전적 초기화", use_container_width=True):
    st.session_state.rps_w = 0
    st.session_state.rps_l = 0
    st.session_state.rps_d = 0
    st.session_state.rps_last = None
    st.info("전적이 초기화되었습니다.")