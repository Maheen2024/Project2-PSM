import streamlit as st
import re
import random
import string
from password_strength import PasswordStats

# Streamlit Page Configuration
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="centered")

# Function to check password strength
def check_password_strength(password):
    stats = PasswordStats(password)
    score = stats.strength() * 100  # Convert to percentage

    # Check for special characters, numbers, and uppercase letters
    special_characters = re.compile(r"[!@#$%^&*(),.?\":{}|<>]")
    has_special = bool(special_characters.search(password))
    has_number = any(char.isdigit() for char in password)
    has_upper = any(char.isupper() for char in password)

    # Adjust scoring
    score += 10 if has_special else -15
    score += 5 if has_number else -10
    score += 5 if has_upper else -10

    # Ensure score stays within 0-100 range
    score = max(0, min(100, score))

    # Determine strength level
    if score < 30:
        return "Very Weak", "🔴"
    elif score < 50:
        return "Weak", "🟠"
    elif score < 70:
        return "Moderate", "🔵"
    else:
        return "Strong", "🟢"

# Function to generate a strong random password
def generate_password(length=16):
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+{}[]<>?"
    return ''.join(random.choice(all_chars) for _ in range(length))

# Callback function to update the password field
def generate_and_update_password():
    new_password = generate_password()
    st.session_state.password_input = new_password
    st.session_state.password_generated = True

    # Store in history
    if "password_history" not in st.session_state:
        st.session_state.password_history = []
    st.session_state.password_history.append(new_password)

# Initialize session state variables if not set
if "password_input" not in st.session_state:
    st.session_state.password_input = ""
if "password_generated" not in st.session_state:
    st.session_state.password_generated = False
if "password_history" not in st.session_state:
    st.session_state.password_history = []

# Streamlit UI
st.title("🔐 Password Strength Meter")
st.write("Is your password strong enough ❓ Let's find out 🔍 if you have a strong password. If not, we will help you create one.")
st.write("Password strength is measured based on complexity and estimated cracking time.")

# Expandable section for password strength categories
with st.expander("🔍 Password Strength Categories"):
    st.markdown("- **🔴 Very Weak:** Passwords that are easily cracked ")
    st.markdown("- **🟠 Weak:** Passwords that are somewhat secure")
    st.markdown("- **🔵 Moderate:** Passwords that are fairly secure")
    st.markdown("- **🟢 Strong:** Passwords that are very secure")

st.write("Enter a password below to check its strength or generate a strong password. 🔍")

# Layout - Ensuring proper alignment
col1, col2 = st.columns([5, 2])  

with col1:
    password = st.text_input(
        "Enter a password:", 
        value=st.session_state.get("password_input", ""), 
        type="password"
    )

with col2:
    st.write("")  # Adds spacing for better alignment
    st.button("🔄 Generate password", on_click=generate_and_update_password, use_container_width=True)

# If a password was generated, show a success message
if st.session_state.password_generated:
    st.success("✅ Generated password added to the input field!")

# Show "Check Password Strength" button only if a password exists
if password:
    if st.button("✅ Check Password Strength"):
        strength, emoji = check_password_strength(password)

        st.write(f"**Strength:** {emoji} {strength}")
        st.progress(PasswordStats(password).strength())

        # Store password in history
        st.session_state.password_history.append(password)

        if strength in ["Very Weak", "Weak"]:
            st.warning("💡 Tips to improve your password:")
            st.markdown("- Use a mix of **uppercase & lowercase letters**")
            st.markdown("- Include **numbers & special characters**")
            st.markdown("- Make it **at least 12 characters long**")
            st.markdown("- Avoid **common words & patterns**")
else:
    st.warning("⚠️ Please enter or generate a password to check its strength.")

# Password History Section
st.markdown("---")
st.subheader("📜 Password History")
if st.session_state.password_history:
    for idx, pw in enumerate(reversed(st.session_state.password_history[-10:]), 1):  # Show last 10 passwords
        st.write(f"{idx}. `{pw}`")
else:
    st.info("No passwords checked or generated yet.")

