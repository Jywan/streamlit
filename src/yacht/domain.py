from __future__ import annotations
from collections import Counter

## 룰/점수 서비스

CATEGORIES = [
    "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
    "Choice", "Four of a Kind", "Full House",
    "Small Straight", "Large Straight", "Yatch"
]

def score_category(dice: list[int], cat: str) -> int:
    cnt = Counter(dice)
    total = sum(dice)

    if cat in {"Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"}:
        face = {"Ones": 1, "Twos": 2, "Threes": 3, "Fours": 4, "Fives": 5, "Sixes": 6}[cat]
        return face * cnt[face]
    
    if cat == "Choice":
        return total

    if cat == "Four of a Kind":
        return total if any(v >= 5 for v in cnt.values()) else 0
    
    if cat == "Full House":
        return total if sorted(cnt.values()) == [2, 3] else 0
    
    if cat == "Small Straight":
        straight = [{1,2,3,4}, {2,3,4,5}, {3,4,5,6}]
        s = set(dice)
        return 15 if any(st_.issubset(s) for st_ in straight) else 0
    
    if cat == "Large Straight":
        s = set(dice)
        return 30 if s == {1,2,3,4,5} or s == {2,3,4,5,6} else 0
    
    if cat == "Yatch":
        return 50 if len(cnt) == 1 else 0
    
    return 0

def total_score(scores: dict[str, int | None]) -> int:
    return sum(v for v in scores.values() if v is not None)

def is_game_over(scores: dict[str, int | None]) -> bool:
    return all(v is not None for v in scores.values())