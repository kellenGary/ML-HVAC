"""
Streamlit HVAC Smart Home Display

A dark-themed smart home interface for monitoring and controlling HVAC settings.
Shows real-time temperature and humidity data with interactive controls.
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
from data_store import SensorDataStore

# Page configuration
st.set_page_config(
    page_title="Smart HVAC Control",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark mode HVAC smart home theme
st.markdown("""
    <style>
    /* Main container */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00d4ff !important;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        color: #00d4ff;
    }
    
    [data-testid="stMetricLabel"] {
        color: #a0a0c0;
        font-size: 1.1rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0091ff 100%);
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.2rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00ffff 0%, #00b4ff 100%);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.5);
        transform: translateY(-2px);
    }
    
    /* Cards */
    div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {
        background: rgba(30, 30, 50, 0.6);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    /* Custom styling for better contrast */
    .element-container {
        color: #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize data store
data_store = SensorDataStore()

# Header
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🏠 Smart HVAC Control Center</h1>", 
            unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0a0c0; font-size: 1.1rem;'>Monitor and control your home climate</p>", 
            unsafe_allow_html=True)

st.markdown("---")

# Get current readings
readings = data_store.get_readings(limit=100)
target_temp = data_store.get_target_temperature()

# Current Status Section
st.markdown("<h2>📊 Current Status</h2>", unsafe_allow_html=True)

if readings:
    latest = readings[-1]
    current_temp = latest['temperature']
    current_humidity = latest['humidity']
    timestamp = datetime.fromisoformat(latest['timestamp'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🌡️ Current Temperature",
            value=f"{current_temp:.1f}°C",
            delta=f"{current_temp * 9/5 + 32:.1f}°F"
        )
    
    with col2:
        st.metric(
            label="💧 Current Humidity",
            value=f"{current_humidity}%",
            delta=None
        )
    
    with col3:
        st.metric(
            label="🎯 Target Temperature",
            value=f"{target_temp:.1f}°C",
            delta=f"{(current_temp - target_temp):.1f}°C"
        )
    
    with col4:
        st.metric(
            label="🕐 Last Update",
            value=timestamp.strftime("%H:%M:%S"),
            delta=None
        )
else:
    st.info("📡 Waiting for sensor data... Make sure the HVAC sensor is running.")

st.markdown("---")

# Temperature Control Section
st.markdown("<h2>🎛️ Temperature Control</h2>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

with col1:
    if st.button("❄️ --", help="Decrease by 1°C"):
        new_temp = target_temp - 1.0
        data_store.set_target_temperature(new_temp)
        st.rerun()

with col2:
    if st.button("🔽 -", help="Decrease by 0.5°C"):
        new_temp = target_temp - 0.5
        data_store.set_target_temperature(new_temp)
        st.rerun()

with col3:
    st.markdown(f"<h2 style='text-align: center; color: #00d4ff; font-size: 3rem; margin: 0;'>{target_temp:.1f}°C</h2>", 
                unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #a0a0c0; margin-top: -10px;'>{target_temp * 9/5 + 32:.1f}°F</p>", 
                unsafe_allow_html=True)

with col4:
    if st.button("🔼 +", help="Increase by 0.5°C"):
        new_temp = target_temp + 0.5
        data_store.set_target_temperature(new_temp)
        st.rerun()

with col5:
    if st.button("🔥 ++", help="Increase by 1°C"):
        new_temp = target_temp + 1.0
        data_store.set_target_temperature(new_temp)
        st.rerun()

st.markdown("---")

# Graphs Section
st.markdown("<h2>📈 Historical Data</h2>", unsafe_allow_html=True)

if len(readings) > 0:
    # Prepare data for plotting
    df = pd.DataFrame(readings)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Create subplots with shared x-axis
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Temperature Over Time', 'Humidity Over Time'),
        vertical_spacing=0.12,
        specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
    )
    
    # Temperature graph
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'],
            y=df['temperature'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#00d4ff', width=3),
            marker=dict(size=6, color='#00d4ff'),
            hovertemplate='<b>Time:</b> %{x|%H:%M:%S}<br><b>Temp:</b> %{y:.1f}°C<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Add target temperature line
    fig.add_hline(
        y=target_temp,
        line_dash="dash",
        line_color="rgba(255, 100, 100, 0.5)",
        annotation_text=f"Target: {target_temp:.1f}°C",
        annotation_position="right",
        row=1, col=1
    )
    
    # Humidity graph
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'],
            y=df['humidity'],
            mode='lines+markers',
            name='Humidity',
            line=dict(color='#00ff9f', width=3),
            marker=dict(size=6, color='#00ff9f'),
            hovertemplate='<b>Time:</b> %{x|%H:%M:%S}<br><b>Humidity:</b> %{y}%<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Update layout for dark theme
    fig.update_layout(
        height=700,
        showlegend=False,
        hovermode='x unified',
        plot_bgcolor='rgba(20, 20, 40, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='#e0e0e0', size=12),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Update x-axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(100, 100, 120, 0.2)',
        showline=True,
        linewidth=2,
        linecolor='rgba(0, 212, 255, 0.3)',
        color='#a0a0c0'
    )
    
    # Update y-axes
    fig.update_yaxes(
        title_text="Temperature (°C)",
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(100, 100, 120, 0.2)',
        showline=True,
        linewidth=2,
        linecolor='rgba(0, 212, 255, 0.3)',
        color='#a0a0c0',
        row=1, col=1
    )
    
    fig.update_yaxes(
        title_text="Humidity (%)",
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(100, 100, 120, 0.2)',
        showline=True,
        linewidth=2,
        linecolor='rgba(0, 212, 255, 0.3)',
        color='#a0a0c0',
        row=2, col=1
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    st.markdown("<h3>📊 Statistics</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📈 Avg Temperature", f"{df['temperature'].mean():.1f}°C")
    with col2:
        st.metric("📉 Min Temperature", f"{df['temperature'].min():.1f}°C")
    with col3:
        st.metric("📈 Max Temperature", f"{df['temperature'].max():.1f}°C")
    with col4:
        st.metric("💧 Avg Humidity", f"{df['humidity'].mean():.0f}%")
else:
    st.info("📊 No data available yet. Start collecting sensor data to see graphs.")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #606070; font-size: 0.9rem;'>🏠 Smart HVAC Control System | "
    f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
    unsafe_allow_html=True
)

# Auto-refresh every 5 seconds
st.markdown("""
    <script>
        setTimeout(function() {
            window.location.reload();
        }, 5000);
    </script>
""", unsafe_allow_html=True)
