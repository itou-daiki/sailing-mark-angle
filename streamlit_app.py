import streamlit as st

st.title("マーク角度計算補助ツール（アップウィンド限定）")

mark_angle = st.number_input("本船から見た上マークの角度（度）", min_value=0.0, max_value=360.0, value=0.0, step=0.1)
close_hauled_angle = st.number_input("自艇のクローズホールドの帆走角度（度）", min_value=0.0, max_value=360.0, value=45.0, step=0.1)

if st.button("計算"):
    relative_angle = mark_angle - close_hauled_angle
    
    # 角度を-180度から180度の範囲に調整
    if relative_angle > 180:
        relative_angle -= 360
    elif relative_angle < -180:
        relative_angle += 360
    
    st.write(f"上マークの相対的な角度: {relative_angle:.1f}度")
    
    if relative_angle > 0:
        st.write("結果: プラス（オーバースタンド）")
    elif relative_angle < 0:
        st.write("結果: マイナス（アンダースタンド）")
    else:
        st.write("結果: ちょうど良い位置")

st.write("注意: この計算はアップウィンドのみを想定しています。")