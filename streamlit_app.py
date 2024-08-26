import streamlit as st

st.title("上マーク角度計算補助ツール")

mark_angle = st.number_input("本船から見た上マークの角度（度）", min_value=0, max_value=360, value=0, step=1)
close_hauled_angle = st.number_input("自艇のクローズホールドの帆走角度（度）", min_value=0, max_value=360, value=45, step=1)
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

st.write("")

st.write(f"上マークと帆走角度の差:")
st.subheader(f" {angle_difference:.1f}°")

st.write("")

if criteria < 45:
    st.write("結果: プラス（良好な位置）")
    st.write("アクション: そのまま帆走を続ける")
elif criteria > 45:
    st.write("結果: マイナス（不適切な位置）")
    st.write("アクション: タックを検討する")
else:
    st.write("結果: イーブン（ちょうど45度）")
    st.write("アクション: 状況に応じて判断（そのまま続けるかタックするか）")

st.write("注意: この計算はアップウィンドのみを想定しています。")
st.write("判定基準:")
st.write("- ポートタック:")
st.write("  • 上マークの角度 - 帆走角度 < 45度: プラス")
st.write("  • 上マークの角度 - 帆走角度 > 45度: マイナス")
st.write("  • 上マークの角度 - 帆走角度 = 45度: イーブン")
st.write("- スターボードタック:")
st.write("  • 帆走角度 - 上マークの角度 < 45度: プラス")
st.write("  • 帆走角度 - 上マークの角度 > 45度: マイナス")
st.write("  • 帆走角度 - 上マークの角度 = 45度: イーブン")