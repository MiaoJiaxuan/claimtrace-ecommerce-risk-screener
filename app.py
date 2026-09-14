import streamlit as st

st.set_page_config(
    page_title="ClaimTrace",
    page_icon="🔎",
    layout="centered",
)

st.title("ClaimTrace")

st.caption(
    "Evidence-grounded screening for Chinese e-commerce advertising claims"
)

st.info(
    "This prototype provides preliminary screening only. "
    "It does not provide legal advice or automatically approve product copy."
)

claim = st.text_area(
    "Chinese product claim",
    placeholder="例如：本产品是全网销量第一的护肤品。",
    height=120,
)

if st.button("Assess claim", type="primary"):
    if not claim.strip():
        st.warning("Please enter a Chinese product claim.")
    else:
        st.success("The interface is working.")

        st.write("Submitted claim:")

        st.code(claim)

        st.warning(
            "Development placeholder: risk assessment, retrieval and citations "
            "have not been connected yet."
        )