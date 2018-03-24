from flask import Flask, redirect, render_template, request, url_for

import helpers
import os
import sys
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)
    if tweets==None or len(tweets)<=0:
        return redirect(url_for("index"))
    
    # absolute paths to lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")
    
    #analyze
    ana=Analyzer(positives,negatives)
    total=0
    positive, negative, neutral = 0.0, 0.0, 100.0
    positiveTemp, negativeTemp=0,0
    for tweet in tweets:
        score=ana.analyze(tweet)
        if score > 0.0:
            positiveTemp+=1
        elif score<0.0:
            negativeTemp+=1
        total+=1
    
    positive=positiveTemp/total
    negative=negativeTemp/total
    neutral=(total-positiveTemp-negativeTemp)/total
    

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
