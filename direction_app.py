import streamlit as st

# Title of our app
st.title("🗺️ Direction Finder")

# Simple explanation
st.write("Choose two locations and I'll help you find the direction!")

# Create two input boxes for locations
start_location = st.text_input("📍 Where are you starting from?", placeholder="e.g., New York, NY")
destination = st.text_input("🎯 Where do you want to go?", placeholder="e.g., Los Angeles, CA")

# Create a button to get directions
if st.button("Get Directions!"):
    # Check if both locations are filled
    if start_location and destination:
        # Show the direction information
        st.success(f"🚀 From: {start_location}")
        st.success(f"🎯 To: {destination}")
        
        # Simple direction message
        st.info("💡 Direction: Travel from your starting point to your destination!")
        
        # Show a simple route suggestion
        st.write("**Suggested Route:**")
        st.write(f"1. Start at {start_location}")
        st.write("2. Plan your journey")
        st.write("3. Arrive at your destination")
        st.write(f"4. Welcome to {destination}!")
        
    else:
        # Show error if locations are missing
        st.error("⚠️ Please fill in both locations!")

# Add some helpful tips
st.markdown("---")
st.write("**💡 Tips:**")
st.write("- Be specific with your locations (city, state/country)")
st.write("- This is a simple direction finder for learning")
st.write("- For real navigation, use Google Maps or similar apps")
