from flask import Flask, render_template, request, jsonify
import openai
import requests

app = Flask(__name__)

# Set API keys (Replace with your actual API keys)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

openai.api_key = OPENAI_API_KEY

# Function to generate a travel itinerary
def generate_itinerary(destination, duration, interests):
    prompt = f"""
    Create a detailed {duration}-day itinerary for {destination} based on these interests: {interests}.
    Include morning, afternoon, and evening activities for each day.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
    )
    return response["choices"][0]["message"]["content"]

# Function to get travel recommendations from SerpAPI (Google Search)
def get_travel_recommendations(destination, interests):
    url = f"https://serpapi.com/search.json?q=top+{interests}+in+{destination}&api_key={SERPAPI_KEY}"
    response = requests.get(url)
    data = response.json()
    places = [result["title"] for result in data.get("organic_results", [])[:5]]
    return places if places else ["No results found"]

# Flask Route for Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Flask API to handle chatbot requests
@app.route("/get_itinerary", methods=["POST"])
def get_itinerary():
    data = request.json
    destination = data.get("destination")
    duration = data.get("duration")
    interests = data.get("interests")

    if not destination or not interests:
        return jsonify({"error": "Please provide all details"}), 400

    recommendations = get_travel_recommendations(destination, interests)
    itinerary = generate_itinerary(destination, duration, interests)

    return jsonify({"recommendations": recommendations, "itinerary": itinerary})

if __name__ == "__main__":
    app.run(debug=True)
