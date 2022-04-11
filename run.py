from flask import Flask, render_template, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
from ast import literal_eval
import random
import squarify
import calendar

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
    
    legend = "text"
    
    # Embed the result in the html output.
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

    ax = plt.plot(groupedByDate.index, groupedByDate.values);

    fig.savefig('./static/images/filmsQuantityByYear.png', bbox_inches = 'tight')

    plt.close(fig)
    
    legend = "Quantité de film par année"
    
    # Embed the result in the html output.
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


def films_quantity_by_genres():
    fig, ax = plt.subplots( nrows=1, ncols=1, figsize=(20,10) )

    genres = pd.DataFrame(df_movies["Genre"].explode().value_counts()).rename(columns={'Genre': 'Quantity'})

    circle = plt.Circle((0,0), 0.7, color='white')

    explode = [0.1 if v == "Adventure" else 0 for v in genres.index]

    ax.pie(genres.Quantity, labels=genres.index, explode=explode, autopct='%1.1f%%', wedgeprops = { 'linewidth' : 2, 'edgecolor' : 'white' });

    p = plt.gcf()

    p.gca().add_artist(circle);

    fig.savefig('./static/images/filmsQuantityByGenres.png', bbox_inches = 'tight')

    plt.close(fig)

    legend = "Quantité de films par genres"

    return {
        "img": "static/images/filmsQuantityByGenres.png",
        "legend": legend 
    }


# def sales_by_genres():
#     genres['Domestic Sales'] = [df_movies[df_movies["Genre"].apply(lambda x : genre in x)]['Domestic Sales (in $)'].sum() for genre in genres.index]
#     genres['International Sales'] = [df_movies[df_movies["Genre"].apply(lambda x : genre in x)]['International Sales (in $)'].sum() for genre in genres.index]
#     genres['World Sales'] = [df_movies[df_movies["Genre"].apply(lambda x : genre in x)]['World Sales (in $)'].sum() for genre in genres.index]
        



@app.route('/genres')
def genres():
    pathFilmsQuantityByGenres = films_quantity_by_genres()
    return render_template(
        'genres.html',
        data={
            'filmsQuantityByGenres': {
                'title': 'Quantité de films par genres',
                'path': pathFilmsQuantityByGenres['img'],
                'legend': pathFilmsQuantityByGenres['legend'],
                'link': 'filmsQuantityByGenres'
            }
        }
    )

@app.cli.command()
def init():
    print("Hello Flask !")

if __name__ == "__main__":
    app.run(debug=True)