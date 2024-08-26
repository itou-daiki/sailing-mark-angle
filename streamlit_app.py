import streamlit as st
import plotly.graph_objects as go
import numpy as np

# (前述のコードは同じなので省略)

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

# (以下のコードは同じなので省略)