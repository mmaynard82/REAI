# prompts.py

def listing_descript_prompt(details: str) -> str:
    """
    Creates a prompt for a compelling real estate listing description.
    """
    return (
        f"You are a professional real estate agent. Create a compelling and descriptive real estate listing description "
        f"for a home based on the following details. Highlight the best features and use enticing language "
        f"to attract potential buyers. Focus on the details provided and make the description suitable for online platforms.\n\n"
        f"Home Details:\n"
        f"---"
        f"{details}"
        f"---"
    )

def plan_sale_prompt(details: str) -> str:
    """
    Creates a prompt for a step-by-step plan for selling a home.
    """
    return (
        f"You are a real estate expert. Give me a step-by-step plan for selling my home in the next 90 days. "
        f"The plan should be detailed and include tips on staging, pricing, timing, marketing, and negotiating. "
        f"My goal is to sell quickly but at a fair price. The home is located in a market with the following characteristics:\n\n"
        f"Market Details:\n"
        f"---"
        f"{details}"
        f"---"
    )

def offer_review_prompt(offer_text: str) -> str:
    """
    Generates a prompt for the Gemini API to review a real estate offer from a PDF.
    """
    return (
        f"You are a professional and helpful real estate assistant. Your task is to analyze a real estate "
        f"offer document and provide a concise, bullet-point summary of its key terms and potential red flags. "
        f"Use the provided text from the offer document to form your analysis.\n\n"
        f"Based on the following offer document text, please provide:\n\n"
        f"1.  **Summary of Key Terms:**\n"
        f"    * Purchase price\n"
        f"    * Contingencies (e.g., financing, inspection, appraisal)\n"
        f"    * Closing date\n"
        f"    * Deposit amount\n"
        f"    * Any other significant terms (e.g., included or excluded items, seller concessions)\n\n"
        f"2.  **Potential Red Flags/Areas for Negotiation:**\n"
        f"    * Identify any clauses that seem unusual or are heavily in favor of the buyer.\n"
        f"    * Highlight any tight deadlines or difficult-to-meet conditions.\n"
        f"    * Suggest a few points that the seller might want to negotiate.\n\n"
        f"Offer Document Text:\n"
        f"---"
        f"{offer_text}"
        f"---"
    )

def roi_prompt(home_features: str) -> str:
    """
    Creates a prompt to suggest home improvements for the best ROI.
    """
    return (
        f"You are a home improvement and real estate expert. Review the following details about a home "
        f"and tell me what improvements should be made before listing to maximize my return on investment (ROI). "
        f"My budget is flexible, but I want to prioritize cost-effective changes. "
        f"Please prioritize curb appeal, bathrooms, and kitchen if relevant.\n\n"
        f"Home Details:\n"
        f"---"
        f"{home_features}"
        f"---"
    )


# prompts.py

# ... (existing prompts)

def offer_comparison_prompt(combined_offers_text: str) -> str:
    """
    Generates a prompt for the Gemini API to compare multiple real estate offers.

    Args:
        combined_offers_text (str): A single string containing the extracted text from all offer documents.

    Returns:
        str: A prompt for the Gemini API.
    """
    return (
        f"You are a professional real estate expert. Your task is to analyze and compare multiple real estate offers side-by-side. "
        f"Based on the following offer documents, provide a detailed comparison in a structured format.\n\n"
        f"Your analysis should cover the following key areas:\n\n"
        f"1.  **Summary Table:** Create a table or a clear bullet-point list that compares the key terms for each offer. "
        f"    Include at least:\n"
        f"    -   Purchase Price\n"
        f"    -   Contingencies (Inspection, Appraisal, Financing)\n"
        f"    -   Closing Date\n"
        f"    -   Earnest Money Deposit (EMD)\n"
        f"    -   Any Seller Concessions (e.g., closing cost credits)\n"
        f"    -   Buyer's Loan Type and Down Payment\n\n"
        f"2.  **Pros and Cons:** For each offer, provide a brief bullet-point list of its key advantages and disadvantages from the seller's perspective.\n\n"
        f"3.  **Overall Recommendation:** Provide a high-level summary and your professional recommendation on which offer is strongest and why. "
        f"    Consider the price, certainty of closing, and timeline.\n\n"
        f"Offer Documents for Comparison:\n"
        f"---"
        f"{combined_offers_text}"
        f"---"
    )