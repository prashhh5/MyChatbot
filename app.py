from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime
import random

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.get_json()
    user_msg = data.get("message", "").lower() # Convert to lowercase for easier checking

    # --- 1. SMART KEYWORD RULES (Makes it feel human) ---
    # This happens BEFORE sentiment analysis
    
    if "time" in user_msg:
        now = datetime.datetime.now().strftime("%H:%M")
        return jsonify({"reply": f"🕒 The current time is {now}.", "score": 0, "sentiment": "Neutral"})
    
    if "your name" in user_msg or "who are you" in user_msg:
        return jsonify({"reply": "🤖 I am the Tier-2 Sentiment Bot, built to win this assignment!", "score": 0.5, "sentiment": "Positive"})

    # --- 2. SENTIMENT ANALYSIS (The Assignment Requirement) ---
    scores = analyzer.polarity_scores(user_msg)
    compound = scores['compound']
    
    # Decide response based on score
    if compound >= 0.5:
        mood = "Very Positive"
        replies = ["That is fantastic!", "I love your energy! 🌟", "Wow, that sounds great!"]
    elif compound > 0.05:
        mood = "Positive"
        replies = ["That sounds good.", "Nice to hear.", "Keep it up!"]
    elif compound <= -0.5:
        mood = "Very Negative"
        replies = ["I am really sorry to hear that. 😢", "That sounds terrible.", "I hope you feel better soon."]
    elif compound < -0.05:
        mood = "Negative"
        replies = ["That is unfortunate.", "Oh no.", "Sorry about that."]
    else:
        mood = "Neutral"
        replies = ["I see.", "Tell me more.", "Interesting."]

    bot_reply = random.choice(replies)

    # We return the REPLY, the SCORE (number), and the MOOD (text)
    return jsonify({
        "reply": bot_reply, 
        "score": compound, 
        "sentiment": mood
    })

if __name__ == "__main__":
    app.run(port=5001, debug=True)

