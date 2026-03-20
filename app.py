import streamlit as st
import random
import time
import os

# --- 页面配置 ---
st.set_page_config(page_title="伤寒论背诵助手", layout="centered")

# --- 自定义样式：宣纸视觉感 ---
st.markdown("""
    <style>
    .main { background-color: #FDF5E6; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #8B0000; color: white; font-weight: bold; }
    .clause-box { background-color: #FFFFFF; border: 2px solid #DEB887; padding: 25px; border-radius: 12px; margin-bottom: 20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    .hu-box { background-color: #FFF8DC; border-left: 6px solid #FF8C00; padding: 18px; margin-top: 15px; border-radius: 4px; }
    .keyword { color: #FF8C00; font-weight: bold; background-color: #FFFFE0; padding: 0 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- 核心逻辑：读取你的 data.txt ---
def load_data():
    clauses = []
    file_path = 'data.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    clauses.append({
                        "section": parts[0],
                        "content": parts[1],
                        "hu": parts[2],
                        "source": parts[3],
                        "level": int(parts[4]) if len(parts) > 4 else 3
                    })
    return clauses

# --- 初始化状态 ---
if 'all_data' not in st.session_state:
    st.session_state.all_data = load_data()
    st.session_state.pool = st.session_state.all_data.copy()
    random.shuffle(st.session_state.pool)
    st.session_state.current = None
    st.session_state.count = 0
    st.session_state.hard_ones = []

# --- 侧边栏：统计进度 ---
with st.sidebar:
    st.header("📊 复习进度")
    total = len(st.session_state.all_data)
    done = st.session_state.count
    st.progress(done / total if total > 0 else 0)
    st.write(f"今日已背：{done} / {total}")
    
    if st.session_state.hard_ones:
        st.subheader("⚠️ 难背条文")
        for h in st.session_state.hard_ones:
            st.caption(f"· {h['source']}: {h['content'][:10]}...")
            
    if st.button("清空进度/重新洗牌"):
        st.session_state.pool = st.session_state.all_data.copy()
        random.shuffle(st.session_state.pool)
        st.session_state.count = 0
        st.session_state.hard_ones = []
        st.rerun()

# --- 主界面 ---
st.title("🏯 《伤寒论》方证背诵")
st.caption("集成胡希恕核心解读 · 随机不重复抽题")

if st.button("抽取下一条"):
    if st.session_state.pool:
        st.session_state.current = st.session_state.pool.pop(0)
        st.session_state.count += 1
        st.session_state.start_time = time.time()
    else:
        st.balloons()
        st.success("恭喜！所有条文已背完！")

# --- 内容展示 ---
if st.session_state.current:
    item = st.session_state.current
    
    # 1. 条文内容展示
    st.markdown(f"""
    <div class="clause-box">
        <div style="color: #8B4513; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid #EEE; padding-bottom: 5px;">
            【{item['section']}】 {item['source']}  &nbsp;&nbsp; 难度：{'⭐'*item['level']}
        </div>
        <div style="font-size: 22px; line-height: 1.6; color: #1A1A1A; font-family: 'KaiTi', '楷体';">
            {item['content']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. 胡希恕解读展示 (自动标黄关键词)
    hu_text = item['hu']
    key_highlights = ["桂枝汤", "表虚证", "表实证", "中风", "伤寒", "麻黄汤", "葛根汤"]
    for k in key_highlights:
        hu_text = hu_text.replace(k, f'<span class="keyword">{k}</span>')
    
    st.markdown(f"""
    <div class="hu-box">
        <div style="font-weight: bold; color: #D2691E; margin-bottom: 8px;">📖 胡希恕核心解读：</div>
        <div style="font-size: 17px; color: #333; line-height: 1.5;">{hu_text}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 3. 耗时逻辑
    duration = int(time.time() - st.session_state.start_time)
    st.caption(f"⏱️ 本条停留时间: {duration} 秒")
    if duration > 300:
        if item not in st.session_state.hard_ones:
            st.session_state.hard_ones.append(item)
        st.warning("这条背太久了，已标记为‘难背’！")
