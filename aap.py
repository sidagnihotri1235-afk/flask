from flask import Flask, request, render_template, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Sample dataset for basic search engine (can be expanded)
DATASET = {
    "python": "Python is a high-level programming language.",
    "flask": "Flask is a lightweight WSGI web application framework in Python.",
    "ai": "Artificial Intelligence is the simulation of human intelligence in machines.",
    "openai": "OpenAI is an AI research and deployment company."
}

def basic_search(query):
    """Simple keyword-based search."""
    results = []
    query = query.lower()
    for key, value in DATASET.items():
        if query in key or query in value.lower():
            results.append(f"{key.title()}: {value}")
    return results if results else ["No results found."]

def logical_reasoning(question):
    """Use OpenAI GPT to perform logical reasoning."""
    prompt = f"Answer the following question logically and clearly:\n{question}"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.5,
            n=1,
            stop=None
        )
        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        return f"Error in reasoning: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get('query', '')
    mode = data.get('mode', 'search')  # 'search' or 'reason'

    if mode == 'search':
        results = basic_search(query)
        return jsonify({'type': 'search', 'results': results})
    elif mode == 'reason':
        answer = logical_reasoning(query)
        return jsonify({'type': 'reason', 'answer': answer})
    else:
        return jsonify({'error': 'Invalid mode'}), 400

if __name__ == '__main__':
    app.run(debug=True)
  
