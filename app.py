import streamlit as st
import joblib
import numpy as np
import matplotlib.pyplot as plt

# Load models
clf_model = joblib.load("Weather-Forecasting/Classification_randomforest.pkl")
reg_model = joblib.load("Weather-Forecasting/optimized_xgb_model.pkl")

# Title and description
st.title("🌦️ Weather Prediction App")
st.markdown(
    "<p style='font-size:16px; color:gray;'>"
    "A simple application to predict rainfall intensity and precipitation volume using machine learning."
    "</p>",
    unsafe_allow_html=True
)

st.divider()

# Sidebar for user input
st.sidebar.header("Enter Weather Details:")
temperature = st.sidebar.number_input("🌡️ Temperature (°C)", value=25.0)
humidity = st.sidebar.number_input("💧 Humidity (%)", value=80.0)
wind_speed = st.sidebar.number_input("🌬️ Wind Speed (m/s)", value=3.5)
wind_deg = st.sidebar.number_input("🧭 Wind Direction (°)", value=180.0)
pressure = st.sidebar.number_input("🔽 Pressure (hPa)", value=1015.0)
clouds = st.sidebar.number_input("☁️ Cloudiness (%)", value=40.0)

input_features = np.array([[temperature, humidity, wind_speed, wind_deg, pressure, clouds]])

if st.sidebar.button("Predict"):
    # Classification Prediction
    prediction_class = clf_model.predict(input_features)
    classification_label = "High" if prediction_class[0] else "Low"
    st.markdown(f"### 🌧️ Rainfall Intensity Prediction: **{classification_label}**")

    # Regression Prediction
    prediction_reg = reg_model.predict(input_features)
    st.markdown(f"### 💦 Predicted Precipitation Volume: **{prediction_reg[0]:.2f} mm**")

    st.divider()

    # Visualizing Results
    st.markdown("#### Weather Conditions vs Predicted Rainfall")
    fig, ax = plt.subplots(figsize=(8, 4))
    bar_labels = ["Temperature", "Humidity", "Wind Speed", "Wind Direction", "Pressure", "Cloudiness"]
    bar_values = [temperature, humidity, wind_speed, wind_deg, pressure, clouds]
    ax.bar(bar_labels, bar_values, color='#0073e6', alpha=0.8, edgecolor='black')
    ax.set_ylabel("Values", fontsize=12)
    ax.set_title("Input Weather Conditions", fontsize=14, fontweight="bold")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    st.divider()

    # Additional Insights
    with st.expander("📌 Additional Insights"):
        st.markdown("- **Humidity:** Higher humidity often increases the chances of precipitation.")
        st.markdown("- **Cloudiness:** Plays a critical role in rainfall prediction.")
        st.markdown("- **Wind Direction and Speed:** Can impact storm formations.")
