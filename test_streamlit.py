import streamlit as st

# Text input box with a custom ID
input_text = st.text_input("Enter text", key="my_input")

# JavaScript to clear the input field after Enter is pressed
script = """
<script>
document.addEventListener("DOMContentLoaded", function(event) {
    const inputElement = document.querySelector(".stTextInput > div > div > input_text");

    inputElement.addEventListener("keypress", function(e) {
        if (e.keyCode === 13) {
            inputElement.value = "";
        }
    });
});
</script>
"""

st.markdown(script, unsafe_allow_html=True)
