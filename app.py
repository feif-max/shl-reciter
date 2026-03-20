import streamlit as st
import random
import time

# 数据源：由 data.txt 完整导入
DATA = [
    {"cap": "太阳病", "id": "1", "txt": "太阳之为病，脉浮，头项强痛而恶寒。", "hu": "胡希恕：太阳病提纲，以此判断表证。",
     "level": 1},
    {"cap": "太阳病", "id": "2", "txt": "太阳病，发热汗出，恶风，脉缓者，名为中风。",
     "hu": "胡希恕：中风即表虚证，汗出是因营卫不和，桂枝汤调和营卫而非发汗。", "level": 3},
    {"cap": "太阳病", "id": "3", "txt": "太阳病，或已发热，或未发热，必恶寒，体痛，呕逆，脉阴阳俱紧者，名为伤寒。",
     "hu": "胡希恕：伤寒即表实证，无汗而喘，须用麻黄汤发汗解表。", "level": 4},
    {"cap": "太阳病", "id": "12",
     "txt": "太阳中风，阳浮而阴弱。阳浮者，热自发；阴弱者，汗自出。啬啬恶寒，淅淅恶风，翕翕发热，鼻鸣干呕者，桂枝汤主之。",
     "hu": "胡希恕：此为中风表虚证。阳浮指卫气浮盛，阴弱指营气不足。", "level": 4},
    {"cap": "太阳病", "id": "13", "txt": "太阳病，头痛发热，汗出恶风，桂枝汤主之。",
     "hu": "胡希恕：此为表虚证，宜桂枝汤调和营卫。", "level": 2},
    {"cap": "太阳病", "id": "53",
     "txt": "病常自汗出者，此为荣气和。荣气和者，外不谐，以卫气不共荣气谐和故尔。以荣行脉中，卫行脉外，复发其汗，荣卫和则愈。",
     "hu": "胡希恕：荣卫不和，复发其汗（调和营卫）则愈。", "level": 3},
    {"cap": "太阳病", "id": "54", "txt": "病人藏无他病，时发热、自汗出而不愈者，此卫气不和也，先其时发汗则愈，宜桂枝汤。",
     "hu": "胡希恕：此为表虚证，宜桂枝汤调和营卫。", "level": 3},
    {"cap": "太阳病", "id": "16(下)", "txt": "桂枝本为解肌，若其人脉浮紧，发热汗不出者，不可与之也。常须识此，勿令误也。",
     "hu": "胡希恕：脉浮紧、汗不出是表实证，禁服桂枝汤。", "level": 5},
    {"cap": "太阳病", "id": "14", "txt": "太阳病，项背强几几，反汗出恶风者，桂枝加葛根汤主之。",
     "hu": "胡希恕：兼项背强几几证，桂枝加葛根汤解肌发表。", "level": 3},
    {"cap": "太阳病", "id": "43", "txt": "太阳病，下之微喘者，表未解故也，桂枝加厚朴杏子汤主之。",
     "hu": "胡希恕：误下后表邪未解且兼喘，加厚朴杏子平喘。", "level": 4},
    {"cap": "太阳病", "id": "18", "txt": "喘家作，桂枝汤加厚朴、杏子佳。", "hu": "胡希恕：喘家外感，桂枝汤平添厚朴杏子。",
     "level": 3},
    {"cap": "太阳病", "id": "20", "txt": "太阳病，发汗，遂漏不止，其人恶风，小便难，四肢微急，难以屈伸者，桂枝加附子汤主之。",
     "hu": "胡希恕：发汗过头伤阳，漏汗不止，加附子固表。", "level": 5},
    {"cap": "太阳病", "id": "21", "txt": "太阳病，下之后，脉促，胸满者，桂枝去芍药汤主之。",
     "hu": "胡希恕：误下后胸满，去芍药以利胸中阳气宣发。", "level": 4},
    {"cap": "太阳病", "id": "62", "txt": "发汗后，身疼痛，脉沉迟者，桂枝加芍药生姜各一两人参三两新加汤主之。",
     "hu": "胡希恕：汗后气营不足身痛，加参、姜、芍补中益气。", "level": 4},
    {"cap": "太阳病", "id": "35", "txt": "太阳病，头痛发热，身疼腰痛，骨节疼痛，恶风无汗而喘者，麻黄汤主之。",
     "hu": "胡希恕：伤寒表实证典型表现，重点在于无汗而喘。", "level": 4},
    {"cap": "太阳病", "id": "36", "txt": "太阳与阳明合病，喘而胸满者，不可下，宜麻黄汤。",
     "hu": "胡希恕：合病表实，喘满不可下，当解表。", "level": 4},
    {"cap": "太阳病", "id": "31", "txt": "太阳病，项背强几几，无汗恶风（者），葛根汤主之。",
     "hu": "胡希恕：表实兼经输不利，葛根汤解肌发汗。", "level": 3},
    {"cap": "太阳病", "id": "32", "txt": "太阳与阳明合病者，必自下利，葛根汤主之。",
     "hu": "胡希恕：合病见下利，葛根汤升津止利。", "level": 3},
    {"cap": "太阳病", "id": "38", "txt": "太阳中风，脉浮紧，发热恶寒，身疼痛，不汗出而烦躁者，大青龙汤主之。",
     "hu": "胡希恕：表实兼阳郁内热，见烦躁者用大青龙。", "level": 5},
    {"cap": "太阳病", "id": "40",
     "txt": "伤寒表不解，心下有水气，干呕，发热而咳，或渴，或利，或噎，或小便不利、少腹满，或喘者，小青龙汤主之。",
     "hu": "胡希恕：表不解兼心下有水气，外散风寒内化水饮。", "level": 5},
    {"cap": "太阳病", "id": "71", "txt": "若脉浮，小便不利，微热消渴者，五苓散主之。", "hu": "胡希恕：太阳蓄水证，化气行水。",
     "level": 4},
    {"cap": "太阳病", "id": "74", "txt": "中风发热，六七日不解而烦，有表里证，渴欲饮水，水入则吐者，名曰水逆，五苓散主之。",
     "hu": "胡希恕：水逆证，五苓散外解表邪，内化水饮。", "level": 4},
    {"cap": "太阳病", "id": "106", "txt": "少腹急结者，乃可攻之，宜桃核承气汤。", "hu": "胡希恕：太阳蓄血轻证，热结膀胱。",
     "level": 4},
    {"cap": "太阳病", "id": "124", "txt": "小便自利者，下血乃愈...以太阳随经，瘀热在里故也，抵当汤主之。",
     "hu": "胡希恕：蓄血重症，瘀热在里。", "level": 5},
    {"cap": "阳明病", "id": "180", "txt": "阳明之为病，胃家实是也。", "hu": "胡希恕：阳明病提纲。胃家实指胃肠燥结、邪热盛。",
     "level": 1},
    {"cap": "阳明病", "id": "182", "txt": "身热，汗自出，不恶寒反恶热也。", "hu": "胡希恕：阳明病外证。热盛于里，故反恶热。",
     "level": 2},
    {"cap": "少阳病", "id": "263", "txt": "少阳之为病，口苦，咽干，目眩也。", "hu": "胡希恕：少阳病提纲。涉及半表半里之热。",
     "level": 1},
    {"cap": "少阳病", "id": "96", "txt": "往来寒热，胸胁苦满，嘿嘿不欲饮食，心烦喜呕...小柴胡汤主之。",
     "hu": "胡希恕：少阳病主方。注意往来寒热、胸胁苦满等四大主证。", "level": 4},
    {"cap": "太阴病", "id": "273", "txt": "太阴之为病，腹满而吐，食不下，自利益甚，时腹自痛。",
     "hu": "胡希恕：太阴病提纲。里虚寒证，脾不化湿。", "level": 3},
    {"cap": "太阴病", "id": "277", "txt": "自利不渴者，属太阴，以其藏有寒故也。当温之，宜服四逆辈。",
     "hu": "胡希恕：藏有寒，当温之。", "level": 3},
    {"cap": "少阴病", "id": "281", "txt": "少阴之为病，脉微细，但欲寐也。", "hu": "胡希恕：少阴病提纲。阳气衰微，精神萎靡。",
     "level": 3},
    {"cap": "少阴病", "id": "323", "txt": "少阴病，脉沉者，急温之，宜四逆场。", "hu": "胡希恕：阴盛阳衰，急温回阳。",
     "level": 4},
    {"cap": "少阴病", "id": "317", "txt": "下利清谷，里寒外热，手足厥逆，脉微欲绝...通脉四逆汤主之。",
     "hu": "胡希恕：阴盛格阳，大剂四逆回阳通脉。", "level": 5},
    {"cap": "厥阴病", "id": "326", "txt": "厥阴之为病，消渴，气上撞心，心中疼热，饥而不欲食，食则吐蚘。下之，利不止。",
     "hu": "胡希恕：厥阴病提纲。寒热错杂。", "level": 5},
    {"cap": "厥阴病", "id": "338", "txt": "蚘厥者，乌梅丸主之。又主久利。", "hu": "胡希恕：蛔厥与脏寒，寒热错杂用乌梅丸。",
     "level": 5},
    {"cap": "差后劳复", "id": "397", "txt": "伤寒解后，虚羸少气，气逆欲吐，竹叶石膏汤主之。",
     "hu": "胡希恕：病后余热未清，气津两伤。", "level": 4}
]

st.set_page_config(page_title="伤寒论背诵助手", layout="centered")

# 设置自定义样式：宣纸背景色感
st.markdown("""
    <style>
    .main { background-color: #FDF5E6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #8B0000; color: white; }
    .stAlert { background-color: #FFF8DC; border: 1px solid #DEB887; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏯 《伤寒论》胡希恕解读背诵")
st.caption("基于方证对应 | 自动统计耗时 | 重点条文标记")

if 'pool' not in st.session_state:
    st.session_state.pool = DATA.copy()
    random.shuffle(st.session_state.pool)
    st.session_state.current = None
    st.session_state.done = []
    st.session_state.hard = []

# 侧边栏
with st.sidebar:
    st.header("📊 学习进度")
    done_num = len(st.session_state.done)
    total_num = len(DATA)
    st.progress(done_num / total_num)
    st.write(f"已背诵: {done_num} / {total_num}")

    if st.session_state.hard:
        st.subheader("⚠️ 难背条文")
        for h in st.session_state.hard:
            st.caption(f"第 {h['id']} 条: {h['txt'][:15]}...")

# 抽取逻辑
if st.button("抽取下一条"):
    if st.session_state.pool:
        st.session_state.current = st.session_state.pool.pop(0)
        st.session_state.start_time = time.time()
    else:
        st.balloons()
        st.success("全部条文背诵完毕！温故而知新。")

# 显示区域
if st.session_state.current:
    c = st.session_state.current
    st.markdown(f"#### 【{c['cap']}】 第 {c['id']} 条")
    st.info(c['txt'])
    st.write(f"难度指数: {'⭐' * c['level']}")

    if st.checkbox("显示核心解读"):
        duration = int(time.time() - st.session_state.start_time)
        st.session_state.done.append(c)

        # 关键词高亮 (胡希恕注重的关键词)
        hu_display = c['hu'].replace("桂枝汤", "**:orange[桂枝汤]**").replace("表虚证", "**:orange[表虚证]**").replace(
            "表实证", "**:red[表实证]**")

        st.warning(f"**胡老解析：**\n\n{hu_display}")
        st.caption(f"本次背诵耗时: {duration} 秒")

        if duration > 300:  # 超过5分钟标记
            if c not in st.session_state.hard:
                st.session_state.hard.append(c)
            st.error("此条背诵耗时过长，已存入难背清单。")