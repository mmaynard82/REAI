import streamlit as st
import google.generativeai as genai
import os
from pypdf import PdfReader
from gemini_api import call_gemini_api
from prompts import listing_descript_prompt, plan_sale_prompt, offer_review_prompt, roi_prompt , offer_comparison_prompt

# Ensure your API key is configured
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

st.title("New Neighbors AI")

choice = st.selectbox("What would you like to do?", [
    "Create a compelling real estate listing description for my home",
    "Give me a step-by-step plan for selling my home in the next 90 days.",
    "Help me review a single offer I received for my home",
    "Compare multiple offers I received for my home",
    "Identify home improvements for best ROI"  # Renamed to match the prompt's purpose
])

if choice == "Create a compelling real estate listing description for my home":
    st.header("Enter Property Details")
    address = st.text_input("Address", placeholder="e.g., 123 Main St, Anytown, USA")
    sqft = st.text_input("Square Footage", placeholder="e.g., 1500")
    beds = st.text_input("Number of Beds", placeholder="e.g., 3")
    baths = st.text_input("Number of Baths", placeholder="e.g., 2.5")
    features = st.text_area("Key Features and Recent Upgrades",
                            placeholder="e.g., Hardwood floors, updated kitchen, new roof, large backyard")
    neighborhood_description = st.text_area("Neighborhood Description",
                                            placeholder="e.g., Quiet cul-de-sac, good schools, close to parks and shopping")

    if st.button("Generate Description"):
        if any([address, sqft, beds, baths, features, neighborhood_description]):
            # Concatenate all inputs into a single string for the prompt
            details = (
                f"Address: {address}\n"
                f"Square Footage: {sqft}\n"
                f"Beds: {beds}\n"
                f"Baths: {baths}\n"
                f"Key Features: {features}\n"
                f"Neighborhood: {neighborhood_description}"
            )

            with st.spinner("Generating description..."):
                description = call_gemini_api(listing_descript_prompt(details))

            st.subheader("🏡 Listing Description")
            st.write(description)
        else:
            st.error("Please fill in at least some details to generate a description.")

elif choice == "Give me a step-by-step plan for selling my home in the next 90 days.":
    st.header("Enter Details for Your Sale Plan")
    market_details = st.text_area("Market and Home Details", height=200,
                                  placeholder="e.g., I live in a competitive market in Austin, TX. The house is a 3-bed, 2-bath, 1950s rancher.")

    if st.button("Generate Sale Plan"):
        if market_details:
            with st.spinner("Generating your personalized plan..."):
                plan = call_gemini_api(plan_sale_prompt(market_details))

            st.subheader("🗓️ 90-Day Sale Plan")
            st.write(plan)
        else:
            st.error("Please provide some market and home details.")

elif choice == "Help me review a single offer I received for my home":
    st.header("Upload Your Offer PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        if st.button("Review Offer"):
            with st.spinner("Reading and analyzing the PDF..."):
                # Read the PDF file
                try:
                    pdf_reader = PdfReader(uploaded_file)
                    offer_text = ""
                    for page in pdf_reader.pages:
                        offer_text += page.extract_text() or ""

                    if offer_text:
                        # Call the Gemini API with the extracted text
                        review = call_gemini_api(offer_review_prompt(offer_text))

                        st.subheader("📝 Offer Review")
                        st.write(review)
                    else:
                        st.error("Could not extract text from the PDF. Please ensure it is not a scanned image.")

                except Exception as e:
                    st.error(f"An error occurred while processing the PDF: {e}")

elif choice == "Compare multiple offers I received for my home":  # New elif block for comparison
    st.header("Upload Multiple Offers for Comparison")
    # Use accept_multiple_files=True to allow uploading more than one file
    uploaded_files = st.file_uploader("Choose multiple PDF offer files", type="pdf", accept_multiple_files=True)

    if uploaded_files:  # Check if the list of uploaded files is not empty
        if st.button("Compare Offers"):
            with st.spinner("Reading and comparing offers..."):
                combined_offers_text = ""
                # Use a dictionary to store offer name and text
                offers_data = {}

                for i, file in enumerate(uploaded_files):
                    try:
                        # Extract text from each PDF
                        pdf_reader = PdfReader(file)
                        offer_text = ""
                        for page in pdf_reader.pages:
                            offer_text += page.extract_text() or ""

                        if offer_text:
                            # Use the file name as a key for the offer
                            offers_data[f"Offer from {file.name}"] = offer_text
                        else:
                            st.warning(f"Could not extract text from {file.name}. Skipping this offer.")
                    except Exception as e:
                        st.error(f"An error occurred while processing {file.name}: {e}")

                if len(offers_data) >= 2:
                    # Combine all extracted texts into a single string
                    for name, text in offers_data.items():
                        combined_offers_text += f"\n\n--- Offer: {name} ---\n{text}\n---------------------\n"

                    # Call the new comparison prompt
                    comparison_result = call_gemini_api(offer_comparison_prompt(combined_offers_text))

                    st.subheader("📊 Offer Comparison")
                    st.write(comparison_result)
                elif len(offers_data) == 1:
                    st.warning("Please upload at least two valid offers to compare.")
                else:
                    st.error("No valid offers were uploaded. Please try again.")


elif choice == "Identify home improvements for best ROI":
    st.header("Identify Improvements for Best ROI")
    home_features = st.text_area("Describe your home's features and current condition", height=200,
                                 placeholder="e.g., 3-bed, 2-bath. Kitchen has older appliances and laminate countertops. The yard is overgrown. I have a budget of around $5,000.")

    if st.button("Get ROI Suggestions"):
        if home_features:
            with st.spinner("Analyzing and suggesting improvements..."):
                roi_suggestions = call_gemini_api(roi_prompt(home_features))

            st.subheader("📈 ROI Suggestions")
            st.write(roi_suggestions)
        else:
            st.error("Please describe your home to get suggestions.")