import google.generativeai as genai
from gemini_api import call_gemini_api
from prompts import listing_descript_prompt, plan_sale_prompt, offer_review_prompt, roi_prompt
from utils import save_to_file
from pypdf import PdfReader  # Import the PdfReader class


# The rest of your imports...


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""  # Handles pages with no text
        return text
    except FileNotFoundError:
        print(f"Error: The file at {pdf_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the PDF: {e}")
        return None


def main():
    print("""
    ---------------------------------------
        Real Estate AI  
    ---------------------------------------
    """)

    while True:
        print("\nChoose an action:")
        print("1. Create a compelling real estate listing description for my home")
        print("2. Give me a step-by-step plan for selling my home in the next 90 days.")
        print("3. Help me review an offer I received for my home.")
        print("4. Compare multiple offers I received for my home.")
        print("5. Increase my ROI on my sale.")
        print("6. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            print("\nEnter the property details:")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == 'END':
                    break
                lines.append(line)
            transcript = "\n".join(lines)
            prompt = listing_descript_prompt(transcript)  # Updated to pass transcript to prompt
            print("\nGenerating Description...")
            summary = call_gemini_api(prompt)
            print("\n--- Listing Description ---")
            print(summary)
            save_to_file("listingdescript.txt", summary)

        elif choice == '2':
            # This section seems to be drafting an email, not a sale plan.
            # I'll assume you intended to update the prompt, so I've updated the call.
            recipient = input("Recipient Name: ")
            project = input("Project Name: ")
            purpose = input("Purpose: ")
            summary = input("Summary: ")
            actions = input("Action Items: ")
            prompt = plan_sale_prompt(recipient, project, purpose, summary,
                                      actions)  # Updated to pass variables to the prompt
            print("\nDrafting email...")
            email = call_gemini_api(prompt)
            print("\n--- Drafted Email ---")
            print(email)

        elif choice == '3':
            pdf_path = input("Enter the path to the PDF offer document: ")

            # Extract text from the PDF
            offer_text = extract_text_from_pdf(pdf_path)

            if offer_text:
                # Use the extracted text to create the prompt
                prompt = offer_review_prompt(offer_text)
                print("\nReviewing offer...")
                review = call_gemini_api(prompt)
                print("\n--- Offer Review ---")
                print(review)
            else:
                print("Could not process the PDF. Please try again.")

        elif choice == '4':  # New comparison logic
            num_offers = int(input("How many offers would you like to compare? "))
            offers_data = {}

            for i in range(num_offers):
                offer_name = input(f"Enter a name for Offer {i + 1} (e.g., 'Offer A', 'Offer from Smith Family'): ")
                pdf_path = input(f"Enter the path to the PDF for '{offer_name}': ")

                offer_text = extract_text_from_pdf(pdf_path)
                if offer_text:
                    offers_data[offer_name] = offer_text
                else:
                    print(f"Warning: Could not process '{offer_name}' PDF. Skipping this offer.")

            if len(offers_data) > 1:
                # Combine all the offer texts into a single string for the prompt
                combined_offers_text = ""
                for name, text in offers_data.items():
                    combined_offers_text += f"\n\n--- Offer: {name} ---\n{text}\n---------------------\n"

                prompt = offer_comparison_prompt(combined_offers_text)
                print("\nComparing offers...")
                comparison_result = call_gemini_api(prompt)
                print("\n--- Offer Comparison ---")
                print(comparison_result)
                save_to_file("offer_comparison.txt", comparison_result)

            elif len(offers_data) == 1:
                print("You only provided one valid offer. Use option 3 for a single offer review.")
            else:
                print("No valid offers were provided. Please try again.")

        elif choice == '5':
            description = input("Project Description: ")
            context = input("Context (optional): ")
            prompt = roi_prompt(description, context)
            print("\nIdentifying risks...")
            risks = call_gemini_api(prompt)
            print("\n--- Risks ---")
            print(risks)

        elif choice == '6':
            print("Exiting Project Management Copilot. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()