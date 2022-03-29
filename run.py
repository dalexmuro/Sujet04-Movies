from flask import Flask, render_template, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
from ast import literal_eval
import random

df_movies = pd.DataFrame(pd.read_csv("data/highest_hollywood_grossing_movies.csv")).iloc[:, 1:]

# Data cleaning
def convert_in_min(row):
    time = row["Movie Runtime"].split(" ")
    hours_in_min = int(time[0]) * 60 
    
    if len(time) >= 3:
        hours_in_min += int(time[2])

    row["Movie Runtime"] = hours_in_min
    return row

df_movies = df_movies.apply(convert_in_min, axis=1)

df_movies["Release Date"] = pd.to_datetime(df_movies["Release Date"], format="%B %d, %Y")

df_movies["Genre"] = df_movies["Genre"].apply(literal_eval)

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template(
        'home.html',
        data={'msg': "Hello world !"}
    )

def plotDistByQuantity(groupedDistributor, count):
    fig, ax = plt.subplots( nrows=1, ncols=1, figsize=(20,10) )

    rgb = [(0.5, random.random(), random.random()) for x in range(count)]
    
    ax.bar(data=groupedDistributor, x=groupedDistributor.index, height="Quantity of movies", color=rgb)
    ax = plt.xticks(rotation = 90);

    fig.savefig('./static/images/barAllDist.png', bbox_inches = 'tight')   # save the figure to file
    plt.close(fig)

    distMostMovies = groupedDistributor.sort_values("Quantity of movies", ascending=False)[:6]


    legend = f"Les 6 plus gros distributeurs qui sont : {', '.join(distMostMovies.index)} ont plus de {round(distMostMovies['Quantity of movies'].sum() / 1000 * 100, 2)}% des films dans le top 1000."
    
    # Embed the result in the html output.
    return {
        "img": "static/images/barAllDist.png",
        "legend": legend
    }

def plotDistBySales(groupedDistributor, count):
    fig, ax = plt.subplots( nrows=1, ncols=1, figsize=(20,10) )

    rgb = [(0, random.random(), random.random()) for x in range(count)]
    
    ax.bar(data=groupedDistributor, x=groupedDistributor.index, height="Average sales by movies", color=rgb)
    ax = plt.xticks(rotation = 90);

    fig.savefig('./static/images/barAllDistBySales.png', bbox_inches = 'tight')   # save the figure to file
    plt.close(fig)
    
    # Embed the result in the html output.
    return "static/images/barAllDistBySales.png"
    

@app.route('/distributors')
def dist():
    grouped = df_movies.groupby("Distributor")
    groupedDistributor = grouped.sum()
    groupedDistributor["Quantity of movies"] = grouped.size()
    groupedDistributor["Average sales by movies"] = groupedDistributor["World Sales (in $)"] / groupedDistributor["Quantity of movies"]
    
    count = len(groupedDistributor.index)
    pathQuantity = plotDistByQuantity(groupedDistributor, count)
    pathSales = plotDistBySales(groupedDistributor, count)

    return render_template('distributors.html', data={
        'quantity' : {
            'title' : 'Quantité de films par distributeurs',
            'path': pathQuantity["img"],
            'legend': pathQuantity["legend"],
            'link' : 'quantity'
        },
        'sales' : {
            'title' : 'Ventes totales de films par distributeurs',
            'path': pathSales,
            'link' : 'sales'
        }
    })

@app.route('/films')
def films():
    return render_template(
        'films.html',
        data={'msg': "Films !"}
    )

@app.route('/genres')
def genres():
    return render_template(
        'genres.html',
        data={'msg': "Genres !"}
    )

@app.cli.command()
def init():
    print("Hello Flask !")

if __name__ == "__main__":
    app.run(debug=True)