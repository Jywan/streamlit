from __future__ import annotations
import json
import streamlit.components.v1 as components

# pip 좌표(0~1 정규화)
PIPS = {
    1: [(0.5, 0.5)],
    2: [(0.25, 0.25), (0.75, 0.75)],
    3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
    4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
    5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
    6: [(0.25, 0.22), (0.25, 0.5), (0.25, 0.78), (0.75, 0.22), (0.75, 0.5), (0.75, 0.78)],
}

def _svg_markup(face: int, size: int = 96) -> str:
    r = max(4, size * 0.06)
    pad = size * 0.12
    inner = size - 2 * pad

    circles = []
    for (x, y) in PIPS[face]:
        cx = pad + inner * x
        cy = pad + inner * y
        circles.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="#111"/>')

    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
        <defs>
            <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="#ffffff"/>
                <stop offset="1" stop-color="#e9e9e9"/>
            </linearGradient>
            <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="rgba(0,0,0,0.35)"/>
            </filter>
        </defs>
        <rect x="4" y="4" width="{size-8}" height="{size-8}" rx="18"
            fill="url(#g)" stroke="rgba(0,0,0,0.15)" filter="url(#shadow)"/>
    {''.join(circles)}
    </svg>
    """.strip()

def render_real_dice(dice_values: list[int], hold_flags: list[bool], roll_id: int):
    payload = {
        "dice": dice_values,
        "hold": hold_flags,
        "rollId": roll_id,
    }
    data = json.dumps(payload)

    # SVG 템플릿은 JS 안에 상수로 둬서(인라인) img/data-uri 의존 제거
    svgs = {str(i): _svg_markup(i, 96) for i in range(1, 7)}
    svgs_json = json.dumps(svgs)

    html = f"""
    <div id="dice-root" data-payload='{data}' style="display:flex; gap:18px; align-items:center;"></div>

    <style>
        .die {{
            width: 96px; height: 96px; border-radius: 18px;
            display:flex; align-items:center; justify-content:center;
            background: rgba(255,255,255,0.02);
            transform-style: preserve-3d;
        }}
        .die.held {{ opacity: 0.55; filter: grayscale(0.35); }}

        @keyframes roll {{
            0%   {{ transform: translateY(0px) rotate(0deg) rotateX(0deg) rotateY(0deg); }}
            15%  {{ transform: translateY(-8px) rotate(16deg) rotateX(55deg) rotateY(35deg); }}
            30%  {{ transform: translateY(3px) rotate(-12deg) rotateX(-50deg) rotateY(70deg); }}
            45%  {{ transform: translateY(-6px) rotate(20deg) rotateX(75deg) rotateY(-50deg); }}
            60%  {{ transform: translateY(4px) rotate(-10deg) rotateX(-60deg) rotateY(45deg); }}
            75%  {{ transform: translateY(-3px) rotate(12deg) rotateX(40deg) rotateY(-35deg); }}
            100% {{ transform: translateY(0px) rotate(0deg) rotateX(0deg) rotateY(0deg); }}
        }}
        .rolling {{ animation: roll 780ms ease-in-out; }}
    </style>

    <script>
        const SVGS = {svgs_json};

        const root = document.getElementById("dice-root");
        const payload = JSON.parse(root.getAttribute("data-payload"));
        const dice = payload.dice;
        const hold = payload.hold;

        root.innerHTML = "";
        const items = [];

        function setFace(i, v) {{
            items[i].wrap.innerHTML = SVGS[String(v)];
        }}

        for (let i = 0; i < 5; i++) {{
            const wrap = document.createElement("div");
            wrap.className = "die" + (hold[i] ? " held" : "");
            root.appendChild(wrap);
            items.push({{wrap}});
            setFace(i, dice[i]);
        }}

        const durationMs = 780;
        const tickMs = 70;
        const ticks = Math.floor(durationMs / tickMs);

        for (let i = 0; i < 5; i++) {{
            if (!hold[i]) items[i].wrap.classList.add("rolling");
        }}

        let t = 0;
        const timer = setInterval(() => {{
            t += 1;
            for (let i = 0; i < 5; i++) {{
                if (!hold[i]) {{
                    const r = 1 + Math.floor(Math.random() * 6);
                    setFace(i, r);
                }}
            }}
        if (t >= ticks) {{
            clearInterval(timer);
            for (let i = 0; i < 5; i++) {{
                setFace(i, dice[i]);
                items[i].wrap.classList.remove("rolling");
                }}
            }}
        }}, tickMs);
    </script>
    """
    components.html(html, height=125)