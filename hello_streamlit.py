import streamlit as st

# Set page config
st.set_page_config(
    page_title="Hello World App",
    page_icon="👋",
    layout="wide"
)

# Main title
st.title("👋 Hello World!")
st.markdown("---")

# Welcome message
st.header("Welcome to Streamlit!")
st.write("This is your first Streamlit application.")

# Add some interactive elements
st.subheader("Interactive Elements")

# Text input
name = st.text_input("What's your name?", placeholder="Enter your name here...")

if name:
    st.success(f"Hello, {name}! Nice to meet you! 🎉")

# Button
if st.button("Click me!"):
    st.balloons()
    st.write("🎉 You clicked the button! Great job!")

# Selectbox
color = st.selectbox(
    "What's your favorite color?",
    ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]
)

st.write(f"You selected: {color}")

# Slider
age = st.slider("How old are you?", 0, 100, 25)
st.write(f"You are {age} years old")

# Sidebar
st.sidebar.title("📋 Menu")
st.sidebar.write("This is the sidebar!")
st.sidebar.write("You can put navigation items here.")

# Add some fun elements
st.markdown("---")
st.subheader("🎨 Fun Elements")

# Columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Temperature", "72°F", "1.2°F")
    
with col2:
    st.metric("Humidity", "45%", "-3%")
    
with col3:
    st.metric("Wind", "8 mph", "2 mph")

# Code block
st.code("""
# This is a code block
print("Hello, Streamlit!")
""", language="python")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
