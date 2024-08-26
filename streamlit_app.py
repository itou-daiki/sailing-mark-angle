import streamlit as st

st.title("マーク角度計算補助ツール（アップウィンド限定）")

mark_angle = st.number_input("本船から見た上マークの角度（度）", min_value=0, max_value=360, value=0, step=1)
close_hauled_angle = st.number_input("自艇のクローズホールドの帆走角度（度）", min_value=0, max_value=360, value=45, step=1)

if st.button("計算"):
    angle_difference = mark_angle - close_hauled_angle
    
    # 角度の差を-180度から180度の範囲に調整
    if angle_difference > 180:
        angle_difference -= 360
    elif angle_difference < -180:
        angle_difference += 360
    
    # 角度の差の絶対値を計算
    abs_angle_difference = abs(angle_difference)
    
    st.write(f"上マークと帆走角度の差: {angle_difference:.1f}度")
    
    if abs_angle_difference < 45:
        st.write("結果: プラス（良好な位置）")
    elif abs_angle_difference > 45:
        st.write("結果: マイナス（不適切な位置）")
    else:
        st.write("結果: イーブン（ちょうど45度）")

st.write("注意: この計算はアップウィンドのみを想定しています。")
st.write("判定基準: 上マークの角度と帆走角度の差が45度以内ならプラス、45度を超えるとマイナス、45度ちょうどならイーブンです。")