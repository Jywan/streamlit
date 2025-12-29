from __future__ import annotations
import random
import streamlit as st
from .domain import CATEGORIES

## 세션/턴 처리 서비스

# 상태 초기화 함수
def init_state():
    ss = st.session_state
    if "y_dice" not in ss:
        ss.y_dice = [random.randint(1, 6) for _ in range(5)]
    if "y_hold" not in ss:
        ss.y_hold = [False] * 5
    if "y_rolls_left" not in ss:
        ss.y_rolls_left = 3
    if "y_scores" not in ss:
        ss.y_scores = {c: None for c in CATEGORIES}
    if "y_message" not in ss:
        ss.y_message = ""
    if "y_roll_id" not in ss:   # 진짜 주사위 렌더 재실행 트리거
        ss.y_roll_id = 0

def reset_turn(keep_message: bool = True):
    ss = st.session_state
    ss.y_dice = [random.randint(1, 6) for _ in range(5)]
    ss.y_hold = [False] * 5
    ss.y_rolls_left = 3
    if not keep_message:
        ss.y_message = ""

def reset_game():
    ss = st.session_state
    ss.y_scores = {c: None for c in CATEGORIES}
    reset_turn(keep_message=False)
    ss.y_message = "NEW GAME"

def roll_dice():
    ss = st.session_state
    if ss.y_rolls_left <= 0:
        ss.y_message = "이번턴은 더이상 굴릴수 없습니다. 카테고리를 선택하세요."
        return
    
    for i in range(5):
        if not ss.y_hold[i]:
            ss.y_dice[i] = random.randint(1, 6)
    
    ss.y_rolls_left -= 1
    ss.y_message = f"굴림 완료. 남은 굴림: {ss.y_rolls_left}"
    ss.y_roll_id += 1  # JS 애니메이션 재실행 신호  
