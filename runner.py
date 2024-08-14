import streamlit as st


st.title("Review Insight", )
st.write(" Automatically summarize product details and analyze customer sentiment for informed purchase decisions")

product_link = st.text_input(label="Product Link:", placeholder="Enter Amazon Product Link:", label_visibility='hidden', key="product_link")

if st.button("Analyze Product"):
    st.write("Analyzing product...")
    # Simulate product data (replace with actual function call)
    product_summary = "This is a versatile product with high durability and user-friendly features."
    st.image("https://via.placeholder.com/150")  # Placeholder for product image
    st.subheader("Product Overview")
    st.write(product_summary)
    if st.button("Analyze Reviews"):
        # Simulate sentiment analysis
        st.subheader("Customer Sentiment Analysis")
        st.write("Overall, customers are highly satisfied with this product.")
        st.write("Based on the analysis, we recommend Buying this product.")
        # Pie chart placeholder
        st.write("Sentiment Distribution: 70% Positive, 20% Neutral, 10% Negative")

        
# Footer
st.write("---")
st.write("Powered by Streamlit & AI Technology")
