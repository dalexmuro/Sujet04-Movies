from flask import Flask, render_template, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
from ast import literal_eval
import random
import squarify
import calendar
import numpy as np
import seaborn as sns
import matplotlib.patches as mpatches


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
    groupedDistributor = groupedDistributor.sort_values("Quantity of movies", ascending=False)

    fig, ax = plt.subplots( nrows=1, ncols=1, figsize=(20,20) )

    rgb = [(0.5, random.random(), random.random()) for x in range(count)]
    
    ax.barh(data=groupedDistributor, width="Quantity of movies", y=groupedDistributor.index, color=rgb)

    plt.margins(y=.01, tight=True)

    fig.savefig('./static/images/barAllDist.png', bbox_inches = 'tight')   # save the figure to file

    distMostMovies = groupedDistributor.sort_values("Quantity of movies", ascending=False)[:6]


    legend = f"Les 6 plus gros distributeurs qui sont : {', '.join(distMostMovies.index)} ont plus de {round(distMostMovies['Quantity of movies'].sum() / 1000 * 100, 2)}% des films dans le top 1000."
    
    # Embed the result in the html output.
    return {
        "img": "static/images/barAllDist.png",
        "legend": legend
    }

def plotDistBySales(groupedDistributor, count):
    groupedDistributor = groupedDistributor.sort_values("Average sales by movies", ascending=False)

    fig, ax = plt.subplots( nrows=1, ncols=1, figsize=(20,20) )

    rgb = [(0, random.random(), random.random()) for x in range(count)]
    
    ax.barh(data=groupedDistributor, width="Average sales by movies", y=groupedDistributor.index, color=rgb)

    plt.margins(y=.01, tight=True)

    fig.savefig('./static/images/barAllDistBySales.png', bbox_inches = 'tight')   # save the figure to file
    
    legend = "text"
    
    return {
        "img": "static/images/barAllDistBySales.png",
        "legend": legend 
        }
    

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
            'path': pathSales["img"],
            'legend': pathSales["legend"],
            'link' : 'sales'
        }
    })


def films_quantity_by_year():
    fig, ax = plt.subplots( nrows=1, ncols=1, figsize=(20,10) )

    groupedByDate = df_movies.groupby(df_movies["Release Date"].dt.year).size()

    ax.bar(x=groupedByDate.index, height=groupedByDate.values)
    
    plt.grid(axis='y')

    plt.xticks(groupedByDate.index)
    ax.set_xticks(groupedByDate.index[::2])
    ax.set_xticklabels(groupedByDate.index[::2].astype(int), rotation=45)
    
    plt.ylabel('Quantité de films')

    plt.margins(x=.01, tight=True)

    fig.savefig('./static/images/filmsQuantityByYear.png', bbox_inches = 'tight')
    
    legend = "Quantité de film par année"
    
    return {
        "img": "static/images/filmsQuantityByYear.png",
        "legend": legend 
    }
    

def films_quantity_by_month():
    fig, ax = plt.subplots( nrows=1, ncols=1, figsize=(20,10) )

    plt.axis('off')

    groupedByMonth = df_movies.groupby(df_movies["Release Date"].dt.month).size()

    labels = [f"{calendar.month_name[i+1]} : {v}" for i, v in enumerate(groupedByMonth)]

    squarify.plot(sizes=groupedByMonth.values, label=labels, alpha=.8, text_kwargs={'fontsize':18}, pad=True);

    fig.savefig('./static/images/filmsQuantityByMonth.png', bbox_inches = 'tight')

    plt.close(fig)

    legend = "Quantité de films sortis par mois"

    return {
        "img": "static/images/filmsQuantityByMonth.png",
        "legend": legend 
    }


@app.route('/films')
def films():
    pathFilmsQuantityByYear = films_quantity_by_year()
    pathFilmsQuantityByMonth = films_quantity_by_month()
    return render_template(
        'films.html',
        data={
                'filmsQuantityByYear': {
                    'title': 'Quantité de film par année',
                    'path': pathFilmsQuantityByYear['img'],
                    'legend': pathFilmsQuantityByYear['legend'],
                    'link': 'filmsQuantityByYear'
                },
                'pathFilmsQuantityByMonth': {
                    'title': 'Quantité de films sortis par mois',
                    'path': pathFilmsQuantityByMonth['img'],
                    'legend': pathFilmsQuantityByMonth['legend'],
                    'link': 'pathFilmsQuantityByMonth'
                }
            }
    )


def films_quantity_by_genres(genres):
    fig = plt.figure(figsize=(20,10))

    ax = plt.subplot(111, polar=True)

    plt.axis('off')

    lowerLimit = 30

    max = genres.Quantity.max()

    slope = (max - lowerLimit) / max

    heights = slope * genres.Quantity + lowerLimit

    width = 2*np.pi / len(genres.index)

    indexes = list(range(1, len(genres.index)+1))
    angles = [element * width for element in indexes]


    bars = ax.bar(
        x=angles, 
        height=heights, 
        width=width, 
        bottom=lowerLimit,
        linewidth=2, 
        edgecolor="white")

    labelPadding = 4

    for bar, angle, height, label in zip(bars,angles, heights, genres.index):
        rotation = np.rad2deg(angle)

        alignment = ""
        if angle >= np.pi/2 and angle < 3*np.pi/2:
            alignment = "right"
            rotation = rotation + 180
        else: 
            alignment = "left"

        ax.text(
            x=angle, 
            y=lowerLimit + bar.get_height() + labelPadding, 
            s=label, 
            ha=alignment, 
            va='center', 
            rotation=rotation, 
            rotation_mode="anchor");

    fig.savefig('./static/images/filmsQuantityByGenres.png', bbox_inches = 'tight')

    plt.close(fig)

    legend = "Quantité de films par genres"

    return {
        "img": "static/images/filmsQuantityByGenres.png",
        "legend": legend 
    }


def films_sales_by_genres(genres):
    genres['Domestic Sales'] = [df_movies[df_movies["Genre"].apply(lambda x : genre in x)]['Domestic Sales (in $)'].sum() for genre in genres.index]
    genres['International Sales'] = [df_movies[df_movies["Genre"].apply(lambda x : genre in x)]['International Sales (in $)'].sum() for genre in genres.index]
    genres['World Sales'] = [df_movies[df_movies["Genre"].apply(lambda x : genre in x)]['World Sales (in $)'].sum() for genre in genres.index]

    fig = plt.figure(figsize=(20, 10))

    sns.barplot(x=genres.index,  y='World Sales', data=genres, color='yellow')
    bar_domestic = sns.barplot(x=genres.index, y='Domestic Sales', data=genres, color='green')
    bar_domestic.set_ylabel('Total World Sales')

    top_bar = mpatches.Patch(color='yellow', label='International Sales')
    bottom_bar = mpatches.Patch(color='green', label='Domestic Sales')
    plt.legend(handles=[top_bar, bottom_bar])

    plt.xticks(rotation = 90)

    fig.savefig('./static/images/filmsSalesByGenres.png', bbox_inches = 'tight')

    plt.close(fig)

    legend = "Ventes de films par genres"

    return {
        "img": "static/images/filmsSalesByGenres.png",
        "legend": legend 
    }
        



@app.route('/genres')
def genres():
    genres = pd.DataFrame(df_movies["Genre"].explode().value_counts()).rename(columns={'Genre': 'Quantity'})

    pathFilmsQuantityByGenres = films_quantity_by_genres(genres)
    pathFilmsSalesByGenres = films_sales_by_genres(genres)

    return render_template(
        'genres.html',
        data={
            'filmsQuantityByGenres': {
                'title': 'Quantité de films par genres',
                'path': pathFilmsQuantityByGenres['img'],
                'legend': pathFilmsQuantityByGenres['legend'],
                'link': 'filmsQuantityByGenres'
            },
            'filmsSalesByGenres': {
                'title': 'Ventes de films par genres',
                'path': pathFilmsSalesByGenres['img'],
                'legend': pathFilmsSalesByGenres['legend'],
                'link': 'filmsSalesByGenres'
            }
        }
    )

@app.cli.command()
def init():
    print("Hello Flask !")

if __name__ == "__main__":
    app.run(debug=True)