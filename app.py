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

    if has_special:
        score += 10  
    else:
        score -= 15  
    
    if has_number:
        score += 5  
    else:
        score -= 10  
    
    if has_upper:
        score += 5  
    else:
        score -= 10  

    # Ensure score stays within valid bounds
    score = max(0, min(100, score))

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
    st.session_state.password_input = generate_password()
    st.session_state.password_generated = True

# Initialize session state variables if not set
if "password_input" not in st.session_state:
    st.session_state.password_input = ""
if "password_generated" not in st.session_state:
    st.session_state.password_generated = False

# Streamlit UI
st.title("🔐 Password Strength Meter")
st.write("Enter a password below to check its strength or generate a strong password. 🔍")

# Layout - Ensuring proper alignment
col1, col2 = st.columns([5, 2])  # Adjust width for better alignment

with col1:
    password = st.text_input(
        "Enter a password:", 
        value=st.session_state.password_input, 
        type="password", 
        key="password_input"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Moves button down slightly for alignment
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

        if strength in ["Very Weak", "Weak"]:
            st.warning("💡 Tips to improve your password:")
            st.markdown("- Use a mix of **uppercase & lowercase letters**")
            st.markdown("- Include **numbers & special characters**")
            st.markdown("- Make it **at least 12 characters long**")
            st.markdown("- Avoid **common words & patterns**")
else:
    st.warning("⚠️ Please enter or generate a password to check its strength.")
