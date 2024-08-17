import streamlit as st
from sentiment_analysis import classify_sentiment, get_sentiment_score
st.set_page_config(page_title="Review Insight", page_icon="	:shopping_trolley:")


st.title("Review Insight")
st.write("Powered by Streamlit & AI Technology")
st.write("---")



uploaded_html = st.file_uploader(label="Upload Product File", type=['html', 'xml'], label_visibility='hidden', key="product_file")

with st.sidebar:
    st.title(" Enter product link:")
    product_link = st.text_input(label="Product link", placeholder="Product Link:", label_visibility='hidden', key="product_link")
    st.warning('Feature down', icon="⚠️")
    


    with st.expander("More information"):
        st.info(
            '''Scraping directly from Amazon is tricky due to its strong anti-scraping measures like rate limiting and CAPTCHA challenges, which often lead to IP blocking after each request.\n\n Without using a paid proxy service, it becomes increasingly challenging. As an alternative, downloading the Amazon link as an HTML file to work with may be a more feasible solution for the time being'''
        )
    st.write('---')
    st.subheader("Instructions")
    st.markdown(" Automatically summarize product details and analyze customer sentiment for informed purchase decisions")





# Footer
st.write("---")
st.write('Refer to the sidebar for more information and instructions')
