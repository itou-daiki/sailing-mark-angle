import streamlit as st
import plotly.graph_objects as go
import numpy as np

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
    result_class = "plus"
    result_text = "プラス（良好な位置）"
    action_text = "そのまま帆走を続ける"
elif criteria > 45:
    result_class = "minus"
    result_text = "マイナス（不適切な位置）"
    action_text = "タックを検討する"
else:
    result_class = "even"
    result_text = "イーブン（ちょうど45度）"
    action_text = "状況に応じて判断（そのまま続けるかタックするか）"

st.markdown(f"<div class='result {result_class}'>", unsafe_allow_html=True)
st.markdown(f"<p class='medium-font'>結果: {result_text}</p>", unsafe_allow_html=True)
st.markdown(f"<p class='small-font'>アクション: {action_text}</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Plotlyを使用した角度の可視化（修正版）
def create_angle_plot(mark_angle, close_hauled_angle, current_tack):
    fig = go.Figure(layout=go.Layout(
        title=go.layout.Title(text="角度の可視化"),
        xaxis=go.layout.XAxis(range=[-1.2, 1.2], showticklabels=False, showgrid=False, zeroline=False),
        yaxis=go.layout.YAxis(range=[-1.2, 1.2], showticklabels=False, showgrid=False, zeroline=False),
        showlegend=False,
        width=400,
        height=400,
        margin=dict(l=0, r=0, t=40, b=0)
    ))

    # 円を描画
    circle_points = np.linspace(0, 2*np.pi, 100)
    x_circle = np.cos(circle_points)
    y_circle = np.sin(circle_points)
    fig.add_trace(go.Scatter(x=x_circle, y=y_circle, mode='lines', line=dict(color='black', width=2)))

    # 風上方向を示す矢印
    fig.add_annotation(x=0, y=1.1, text="風上", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='purple')

    # 角度を調整（風上を0度とする）
    adjusted_mark_angle = (90 - mark_angle) % 360
    adjusted_close_hauled_angle = (90 - close_hauled_angle) % 360

    # 帆走角度の線を描画
    x_close_hauled = [0, np.cos(np.radians(adjusted_close_hauled_angle))]
    y_close_hauled = [0, np.sin(np.radians(adjusted_close_hauled_angle))]
    fig.add_trace(go.Scatter(x=x_close_hauled, y=y_close_hauled, mode='lines', line=dict(color='blue', width=2, dash='dash')))

    # マーク角度の線を描画
    x_mark = [0, np.cos(np.radians(adjusted_mark_angle))]
    y_mark = [0, np.sin(np.radians(adjusted_mark_angle))]
    fig.add_trace(go.Scatter(x=x_mark, y=y_mark, mode='lines', line=dict(color='red', width=2)))

    # 角度差の扇形を描画
    if current_tack == "ポート":
        start_angle = adjusted_close_hauled_angle
        end_angle = adjusted_mark_angle
    else:
        start_angle = adjusted_mark_angle
        end_angle = adjusted_close_hauled_angle
    
    if start_angle > end_angle:
        start_angle, end_angle = end_angle, start_angle

    angle_diff = np.linspace(start_angle, end_angle, 50)
    x_diff = np.cos(np.radians(angle_diff))
    y_diff = np.sin(np.radians(angle_diff))
    fig.add_trace(go.Scatter(x=x_diff, y=y_diff, fill='tozeroy', fillcolor='rgba(0, 255, 0, 0.2)', mode='lines', line=dict(color='green', width=0)))

    # 注釈を追加
    fig.add_annotation(x=0.7*np.cos(np.radians(adjusted_close_hauled_angle)), 
                       y=0.7*np.sin(np.radians(adjusted_close_hauled_angle)),
                       text="帆走角度", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='blue')
    fig.add_annotation(x=0.7*np.cos(np.radians(adjusted_mark_angle)), 
                       y=0.7*np.sin(np.radians(adjusted_mark_angle)),
                       text="マーク角度", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='red')

    return fig

# 角度の可視化を表示
st.plotly_chart(create_angle_plot(mark_angle, close_hauled_angle, current_tack))

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