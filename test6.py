import openai
from openai.error import OpenAIError

# Replace with your actual OpenAI API key
openai.api_key = ""

def rephrase_message(buyer_name, seller_name, store_name, product_title, buyer_question, seller_response):
    try:
        prompt = f"""
        You are a professional eBay seller handling customer queries with a polite and professional tone.  
        Your task is to rephrase the following response into a well-structured and professional reply while keeping the key details intact. Ensure that the response follows this structure:
        1. Greet the buyer by name.  
        2. Introduce yourself and your store.  
        3. Ask about the buyer’s well-being.  
        4. Provide a clear and professional answer to the query.  
        5. End with a polite closing, including your name and store name.  

        Product Title: {product_title}  
        Buyer Name: {buyer_name}  
        Seller Name: {seller_name}  
        Store Name: {store_name}  

        Buyer’s Question: "{buyer_question}"  
        Seller’s Response: "{seller_response}"  
        """

        response = openai.Completion.create(
            model="gpt-4o-mini",  # You can also use "gpt-4" if required
            prompt=prompt,
            max_tokens=250
        )

        # Get the rephrased response text
        return response.choices[0].text.strip()

    except OpenAIError as e:
        return f"Error communicating with OpenAI API: {e}"

    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Example usage
buyer_name = "Sheldon"
seller_name = "Rahul"
store_name = "JewelPalace"
product_title = "SKAVIJ Men's Red Tunic Art Silk Kurta Pajama Indian Wedding 2 Piece Set"
buyer_question = "Pajama is made up of which fabric?"
seller_response = "Cotton"

rephrased_message = rephrase_message(buyer_name, seller_name, store_name, product_title, buyer_question, seller_response)
print(rephrased_message)
