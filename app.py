import streamlit as st


def estimate_risk(air_temperature, process_temperature, rotational_speed, torque, tool_wear):
    """Return a transparent rule-based risk estimate, not an ML prediction."""
    score = 5
    reasons = []
    temperature_gap = process_temperature - air_temperature

    if tool_wear >= 200:
        score += 35
        reasons.append("Tool wear is high (200 minutes or more).")
    elif tool_wear >= 150:
        score += 20
        reasons.append("Tool wear needs closer monitoring.")
    if torque >= 65:
        score += 25
        reasons.append("Torque is above the normal operating range.")
    elif torque <= 15:
        score += 15
        reasons.append("Torque is unusually low.")
    if rotational_speed >= 2500:
        score += 20
        reasons.append("Rotational speed is high.")
    elif rotational_speed <= 1000:
        score += 10
        reasons.append("Rotational speed is low.")
    if temperature_gap < 8 or temperature_gap > 12:
        score += 15
        reasons.append("The process-to-air temperature difference is unusual.")
    if not reasons:
        reasons.append("All readings are within the normal ranges used by this checker.")
    return min(score, 100), reasons


st.set_page_config(page_title="Machine Risk Checker", page_icon=":material/settings:", layout="centered")
st.title("Machine Maintenance Risk Checker")
st.write("Enter the current readings to get a transparent, rule-based maintenance-risk estimate.")

with st.form("machine_readings"):
    left, right = st.columns(2)
    with left:
        st.selectbox("Machine type", options=["L", "M", "H"], index=1)
        air_temperature = st.number_input("Air temperature (K)", 250.0, 400.0, 300.0, 0.1)
        rotational_speed = st.number_input("Rotational speed (rpm)", 0, 10000, 1500, 10)
    with right:
        process_temperature = st.number_input("Process temperature (K)", 250.0, 450.0, 310.0, 0.1)
        torque = st.number_input("Torque (Nm)", 0.0, 200.0, 45.0, 0.1)
        tool_wear = st.number_input("Tool wear (min)", 0, 1000, 100, 1)
    submitted = st.form_submit_button("Check maintenance risk", type="primary", use_container_width=True)

if submitted:
    risk_score, reasons = estimate_risk(air_temperature, process_temperature, rotational_speed, torque, tool_wear)
    st.divider()
    st.metric("Estimated maintenance risk", f"{risk_score}%")
    if risk_score >= 70:
        st.error("High risk: perform urgent preventive maintenance.")
    elif risk_score >= 35:
        st.warning("Medium risk: schedule an inspection within 7 days.")
    else:
        st.success("Low risk: continue normal monitoring.")
    st.subheader("Why this result?")
    for reason in reasons:
        st.write(f"- {reason}")

st.caption("This is a rule-based estimate, not a machine-learning model prediction.")
