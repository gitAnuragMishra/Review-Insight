import streamlit as st
from sentiment_analysis import classify_overall_sentiment, get_star_rating, aggregate_sentiment_scores
from html_handler import extract_product_name, extract_reviews_from_files, save_uploaded_file, extract_product_descriptions_from_folder
from summariser import summarise
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

atexit.register(cleanup)


def landing_page():
    st.set_page_config(page_title="Review Insight", page_icon="	:shopping_trolley:")
    st.header("Review Insight :shopping_trolley:", divider=True)
    #st.subheader("Powered by Streamlit & AI Technology")
    st.markdown(" ##### Automatically summarize product details and analyze customer sentiment for informed purchase decisions")
    st.write("---")



    uploaded_html_files = st.file_uploader(label="Upload Product File", type=['html', 'xml'], label_visibility='hidden', key="product_file", accept_multiple_files=True) #going to accept multiple files, like we are forced to upload multiple files as the code has been written keeping in mind that 'uploaded_files' is a list
    is_disabled = uploaded_html_files is None or len(uploaded_html_files) == 0 

    if 'extraction_complete' not in st.session_state:
        st.session_state['extraction_complete'] = False #initialising extraction session state

    if st.button('Extract from HTML', disabled=is_disabled):
        #save html file ------------------------#
        save_uploaded_file(uploaded_html_files, config['html_file_path'])

        #extract product name(s)-------------------------#
        product_names = extract_product_name(uploaded_html_files)
        names_json_path = os.path.join(config['html_file_path'], "extracted_names.json")
        with open(names_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(product_names, json_file, ensure_ascii=False, indent=4)

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

        st.success("Extraction completed. Now click 'Analyze' to view results.")
        st.session_state['extraction_complete'] = True
    
    analyze_disabled = not st.session_state['extraction_complete'] #currently false

    if st.button('Analyze', disabled= analyze_disabled) and os.path.exists(os.path.join(config['html_file_path'], "extracted_names.json")):
        #important to note
        #when we get 'back' from analysis page, the extract from html button wont be active but analyse button will be, as there exists extracted files in the html folder       
        st.session_state['page'] = 2
        st.rerun()  # Force a rerun to redirect



    with st.sidebar:
        st.title(" Enter product link:")
        product_link = st.text_input(label="Product link", placeholder="Product Link:", label_visibility='hidden', key="product_link")
        st.warning('Feature down', icon="⚠️")
        

        with st.expander("More information"):
            st.info(
                '''Scraping directly from Amazon is tricky due to its strong anti-scraping measures like rate limiting and CAPTCHA challenges, which often lead to IP blocking after each request.\n\n Without using a paid proxy service, it becomes increasingly challenging. As an alternative, downloading the Amazon link as an HTML file to work with may be a more feasible solution for the time being'''
            )
        st.write('---')

        if st.button('Instruction Page'):
            st.session_state['page'] = 3
            st.rerun()
        
        



    # Footer
    st.write("---")
    st.write('Refer to the sidebar for more information and instructions')


def analysis_page():
    st.set_page_config(page_title="Review Insight - Analysis", page_icon=":shopping_trolley:")
    st.header("Product Analysis Results :bar_chart:", divider=True)
    st.markdown(" #### Here are the summarized product details and sentiment analysis:")
    st.write("---")

    # Load the JSON files containing the analysis results
    names_json_path = os.path.join(config['html_file_path'], "extracted_names.json")
    review_json_path = os.path.join(config['html_file_path'], "extracted_reviews.json")
    description_json_path = os.path.join(config['html_file_path'], "extracted_descriptions.json")

    if os.path.exists(names_json_path) and os.path.exists(review_json_path) and os.path.exists(description_json_path):
        with open(names_json_path, 'r', encoding='utf-8') as file:
            product_names = json.load(file)
        with open(review_json_path, 'r', encoding='utf-8') as file:
            all_reviews = json.load(file)
        with open(description_json_path, 'r', encoding='utf-8') as file:
            all_description = json.load(file)
        with st.spinner('Analyzing...'):
        # Display the results
            summarized_descriptions = [summarise(desc) for desc in all_description]
            summarized_reviews = [summarise(review) for review in all_reviews]
            # aggregated_scores = [aggregate_sentiment_scores(review) for review in all_reviews]
            # overall_sentiment = [classify_overall_sentiment(review) for review in all_reviews]
            # print(aggregated_scores, overall_sentiment)
            aggregated_scores, overall_sentiment = classify_overall_sentiment(all_reviews)
            for  name, desc_summary, review_summary in zip( product_names, summarized_descriptions, summarized_reviews):
                #python .zip function, takes .zip(list1, list2, list3)
                

                st.markdown(f"##### {name}")
                st.write(f"##### Product Summary:\n")
                st.write(f" {desc_summary}\n")
                st.markdown("##### Review Summary:\n")
                st.write(f"{review_summary}\n")
                st.markdown("##### Overall buyer sentiment:\n")
                
                st.write(f"The buyers are **{overall_sentiment}** of the product with an overall sentiment score of:  \n **Positive sentiment** {aggregated_scores.get('roberta_pos', 0):.2f}  \n **Neutral sentiment** {aggregated_scores.get('roberta_neu', 0):.2f}   \n **Negative sentiment** {aggregated_scores.get('roberta_neg', 0):.2f}  \n")
                # st.write(f"The buyers are {overall_sentiment} with overall sentiment score of {aggregated_scores} normalised to {normalised_score}/10.\n")
                st.markdown("##### Verdict: \n")
                st.write(f"Sentiment Rating: {get_star_rating(aggregated_scores)}")
            # st.write(aggregated_scores, overall_sentiment)


    else:
        st.warning("Analysis data not found. Please go back and analyze a product.")

    # Button to go back to the first page
    if st.button("Go Back"):
        st.session_state['page'] = 1
        cleanup()
        st.rerun() 
        ##IMPORTANT: DO NOT RERUN, as the summarisation will rerun, taking up a lot of time

def steps_page():
    st.set_page_config(page_title="Review Insight - Instructions", page_icon=":shopping_trolley:")
    st.header("Instructions ", divider=True)
    st.markdown("""
    #### How to Download the .html File from an Amazon Product Page:

    1. **Open the Amazon Product Page**:
       - In your web browser, navigate to the Amazon product page that you want to analyze.

    2. **Save the Webpage as HTML**:
       - Right-click on the page and select **Save as...** from the context menu.
       - Else, click **CTRL + S**.
       - In the dialog that opens, choose **Webpage, HTML Only (*.html,*.htm)** as the format.
       - Save the file to your computer. This will save the *.html* file at your desired location.

    3. **Upload the HTML File**:
       - Return to the Review Insight app and use the "Upload Product File" button to upload the *.html* file you just saved.
       - The app supports uploading multiple HTML files if you want to analyze more than one product at a time.

    4. **Extract Data and Analyze**:
       - Follow the on-screen instructions in the app to extract data and analyze the product details.

    #### Notes:
    - **Product Link Feature**: Currently, the product link feature is down due to Amazon's strong anti-scraping measures without a paid proxy service.
    """)
    if st.button("Go Back"):
        st.session_state['page'] = 1
        st.rerun()



def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 1 #initialising session state

    if st.session_state['page'] == 1:
        landing_page()
    elif st.session_state['page'] == 2:
        analysis_page()

    elif st.session_state['page'] == 3:
        steps_page()
    




if __name__ == '__main__':
    main()