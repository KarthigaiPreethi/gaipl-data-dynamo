import openai
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Set up your OpenAI API key
openai.api_key = 'your-api-key-here'

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

        # Call the OpenAI API to generate a response
        response = openai.Completion.create(
            model="gpt-4",  # You can use other models like gpt-3.5-turbo
            prompt=prompt,
            max_tokens=150
        )

        # Extract the text from the response
        response_text = response.choices[0].text.strip()

        # Return the response text as JSON
        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the server
if __name__ == "__main__":
    app.run(debug=True)
