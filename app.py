import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Language Translator App", page_icon="⚡", layout="centered")

@st.cache_data
def get_languages():
    return GoogleTranslator().get_supported_languages(as_dict=True)

def main():
    st.title("Language Translator App")
    st.markdown("---")

    languages_dict = get_languages()
    language_names = list(languages_dict.keys())
    
    display_names = [name.title() for name in language_names]
    
    try:
        default_index = display_names.index("English")
    except ValueError:
        default_index = 0
    
    col_src, col_tgt = st.columns(2)

    with col_src:
        st.info("From: Auto (Detected)")

    with col_tgt:
        selected_display_name = st.selectbox(
            "To:",
            options=display_names,
            index=default_index,
            label_visibility="collapsed" 
        )
        st.caption(f"Target: {selected_display_name}")

    target_lang_key = selected_display_name.lower()

    text_input = st.text_area(
        "Enter text to translate:", 
        height=150, 
        placeholder="Type something here..."
    )

    b1, b2, b3 = st.columns([1, 1, 1])
    
    if b2.button("Translate", type="primary", use_container_width=True):
        if not text_input:
            st.warning("Please enter some text to translate.")
        else:
            try:
                with st.spinner(f"Translating to {selected_display_name}..."):
                    
                    translator = GoogleTranslator(source='auto', target=target_lang_key)
                    
                    translation = translator.translate(text_input)
                    
                    st.markdown("### Results")
                    
                    res_col1, res_col2 = st.columns(2)
                    
                    with res_col1:
                        st.caption("Original")
                        st.info(text_input)
                        
                    with res_col2:
                        st.caption(f"Translated ({selected_display_name})")
                        st.success(translation)
                        
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()