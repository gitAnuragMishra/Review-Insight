import streamlit as st
from sentiment_analysis import classify_sentiment, get_sentiment_score
from html_handler import extract_reviews_from_files, save_uploaded_file, extract_product_descriptions_from_folder
import yaml #type: ignore
import atexit
import os
import shutil
import json


with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

def cleanup(): 
    if os.path.exists(config['html_file_path']):
        shutil.rmtree(config['html_file_path'])
        print('Deleted html files at ' + config['html_file_path'])

def main():
    st.set_page_config(page_title="Review Insight", page_icon="	:shopping_trolley:")
    st.header("Review Insight :shopping_trolley:", divider=True)
    st.subheader("Powered by Streamlit & AI Technology")
    st.markdown(" Automatically summarize product details and analyze customer sentiment for informed purchase decisions")
    st.write("---")



    uploaded_html_files = st.file_uploader(label="Upload Product File", type=['html', 'xml'], label_visibility='hidden', key="product_file", accept_multiple_files=True)


    if st.button('Analyze') and uploaded_html_files is not None:
        #save html file ------------------------#
        save_uploaded_file(uploaded_html_files, config['html_file_path'])

        #extract and save reviews-------------------------#
        all_reviews = extract_reviews_from_files(config['html_file_path'])
        review_json_path = os.path.join(config['html_file_path'], "extracted_reviews.json")
        with open(review_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(all_reviews, json_file, ensure_ascii=False, indent=4)

        #extract and save product details-------------------------#
        all_description = extract_product_descriptions_from_folder(config['html_file_path'])
        description_json_path = os.path.join(config['html_file_path'], "extracted_descriptions.json")
        with open(description_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(all_description, json_file, ensure_ascii=False, indent=4)

        
        



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
        





    # Footer
    st.write("---")
    st.write('Refer to the sidebar for more information and instructions')

    atexit.register(cleanup)



if __name__ == '__main__':
    main()