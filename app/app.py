from flask import Flask, render_template, request
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == "POST":
        inp = request.form.get("inp")
        sid = SentimentIntensityAnalyzer()
        score = sid.polarity_scores(inp)
        if score['neg'] != 0:
            return render_template('home.html', message="Negative 😥😥 ", score=score)
        # if score['neu'] !=0.5:
        #     return render_template('home.html', message="Neutral 😑😑 ", score=score)
        else:
            return render_template('home.html', message='Positive 😋😋', score=score)
    return render_template('home.html')
