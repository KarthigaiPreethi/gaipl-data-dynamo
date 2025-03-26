import openai
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Set up your OpenAI API key
openai.api_key = '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'

# Example custom dataset
dataset = {
    "What is the capital of France?": "The capital of France is Paris.",
    "Who is the president of the United States?": "The president of the United States is Joe Biden.",
    "What is the tallest mountain in the world?": "The tallest mountain in the world is Mount Everest."
}

# Function to get a custom answer from the dataset
def get_custom_answer(prompt):
    return dataset.get(prompt, None)

# Create a route that will handle POST requests
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Get the prompt from the request body
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "Prompt is required!"}), 400

        # First, check if the prompt exists in the custom dataset
        custom_answer = get_custom_answer(prompt)

        if custom_answer:
            # If a custom answer exists, return it
            return jsonify({"response": custom_answer})

        # If no custom answer is found, fall back to the OpenAI API
        response = openai.ChatCompletion.create(            model="gpt-4",  # Or another model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )

        # Extract and return the response from OpenAI
        response_text = response['choices'][0]['message']['content'].strip()

        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the server
if __name__ == "__main__":
    app.run(debug=True)
