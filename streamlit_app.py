import streamlit as st

# ページ設定
st.set_page_config(page_title="上マーク角度計算補助ツール", layout="wide")

# カスタムCSS
st.markdown("""
<style>
    .big-font {font-size:30px !important; font-weight:bold;}
    .medium-font {font-size:24px !important;}
    .small-font {font-size:18px !important;}
    .result {padding: 20px; border-radius: 10px; margin-bottom: 20px;}
    .plus {background-color: #d4edda; color: #155724;}
    .minus {background-color: #f8d7da; color: #721c24;}
    .even {background-color: #fff3cd; color: #856404;}
</style>
""", unsafe_allow_html=True)

st.title("⛵ 上マーク角度計算補助ツール")

col1, col2 = st.columns(2)

with col1:
    mark_angle = st.number_input("本船から見た上マークの角度（度）", min_value=0, max_value=360, value=0, step=1)
    close_hauled_angle = st.number_input("自艇のクローズホールドの帆走角度（度）", min_value=0, max_value=360, value=45, step=1)

with col2:
    current_tack = st.radio("現在のタック", ("ポート", "スターボード"))

# 角度の差を計算
angle_difference = mark_angle - close_hauled_angle

# 角度の差を-180度から180度の範囲に調整
if angle_difference > 180:
    angle_difference -= 360
elif angle_difference < -180:
    angle_difference += 360

# タックに応じて判定基準を調整
if current_tack == "ポート":
    criteria = angle_difference
else:  # スターボードの場合
    criteria = -angle_difference

st.markdown("<p class='big-font'>上マークと帆走角度の差:</p>", unsafe_allow_html=True)
st.markdown(f"<p class='medium-font'>{angle_difference:.1f}°</p>", unsafe_allow_html=True)

if criteria < 45:
    st.markdown("<div class='result plus'>", unsafe_allow_html=True)
    st.markdown("<p class='medium-font'>結果: プラス（良好な位置）</p>", unsafe_allow_html=True)
    st.markdown("<p class='small-font'>アクション: そのまま帆走を続ける</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
elif criteria > 45:
    st.markdown("<div class='result minus'>", unsafe_allow_html=True)
    st.markdown("<p class='medium-font'>結果: マイナス（不適切な位置）</p>", unsafe_allow_html=True)
    st.markdown("<p class='small-font'>アクション: タックを検討する</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='result even'>", unsafe_allow_html=True)
    st.markdown("<p class='medium-font'>結果: イーブン（ちょうど45度）</p>", unsafe_allow_html=True)
    st.markdown("<p class='small-font'>アクション: 状況に応じて判断（そのまま続けるかタックするか）</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p class='small-font'>注意: この計算はアップウィンドのみを想定しています。</p>", unsafe_allow_html=True)

with st.expander("判定基準の詳細"):
    st.write("- ポートタック:")
    st.write("  • 上マークの角度 - 帆走角度 < 45度: プラス")
    st.write("  • 上マークの角度 - 帆走角度 > 45度: マイナス")
    st.write("  • 上マークの角度 - 帆走角度 = 45度: イーブン")
    st.write("- スターボードタック:")
    st.write("  • 帆走角度 - 上マークの角度 < 45度: プラス")
    st.write("  • 帆走角度 - 上マークの角度 > 45度: マイナス")
    st.write("  • 帆走角度 - 上マークの角度 = 45度: イーブン")