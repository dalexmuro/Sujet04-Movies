from flask import Flask, render_template
import base64
from io import BytesIO

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ast import literal_eval
import matplotlib.patches as mpatches

df_movies = pd.DataFrame(pd.read_csv("data/highest_hollywood_grossing_movies.csv")).iloc[:, 1:]

def convert_in_min(row):
    time = row["Movie Runtime"].split(" ")
    hours_in_min = int(time[0]) * 60 
    
    if len(time) >= 3:
        hours_in_min += int(time[2])
    # try:
    #     hours_in_min += int(time[2])
    # except:
    #     pass
    row["Movie Runtime"] = hours_in_min
    return row

df_movies = df_movies.apply(convert_in_min, axis=1)

df_movies["Release Date"] = pd.to_datetime(df_movies["Release Date"], format="%B %d, %Y")

df_movies["Genre"] = df_movies["Genre"].apply(literal_eval)

app = Flask(__name__)

@app.route('/')
def index():
    # df_cdrs.head()
    # df_cdrs.tail()
    return "Hello world !"

def plotDistByQuantity(groupedDistributor):
    fig, ax = plt.subplots( nrows=1, ncols=1, figsize=(20,10) )
    
    ax.bar(data=groupedDistributor, x=groupedDistributor.index, height="Quantity of movies")
    ax = plt.xticks(rotation = 90);

    fig.savefig('./static/images/barAllDist.png', bbox_inches = 'tight')   # save the figure to file
    plt.close(fig)
    
    # Embed the result in the html output.
    return "static/images/barplotDist.png"

def plotDistBySales(groupedDistributor):
    fig, ax = plt.subplots( nrows=1, ncols=1, figsize=(20,10) )
    
    ax.bar(data=groupedDistributor, x=groupedDistributor.index, height="Average sales by movies")
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
    
    pathQuantity = plotDistByQuantity(groupedDistributor)
    pathSales = plotDistBySales(groupedDistributor)

    return render_template('distributors.html',
                            data={'quantity' : {'title' : 'Quantité de films par distributeurs',
                                                'path': pathQuantity
                                                },
                                  'sales' : {'title' : 'Ventes totales de films par distributeurs',
                                                'path': pathSales
                                                }
                                   }
                            )


# @app.route("/titanic/<survived>", methods=("POST", "GET"))
# def album(survived=None):
#     survived = int(survived)
#     mask = (titanic.survived == survived)

#     print(titanic[mask].values)

#     return render_template('index.html',
#                            count=mask.sum(),
#                            persons=titanic[mask].values,
#                            titles=titanic.columns.values
#                            )

@app.cli.command()
def init():
    print("Hello Flask !")

if __name__ == "__main__":
    app.run(debug=True)