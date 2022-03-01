from flask import Flask, render_template
import base64
from io import BytesIO

import pandas as pd
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt

df_cdrs = pd.DataFrame(pd.read_csv("data/highest_hollywood_grossing_movies.csv"))

app = Flask(__name__)

@app.route('/')
def index():
    # df_cdrs.head()
    # df_cdrs.tail()
    return "Hello world !"

# @app.route("/line")
# def test():
#     fig = plt.Figure()
#     fig.set_canvas(plt.gcf().canvas)
#     ax = fig.subplots()
#     ax.plot([1, 2])
#     # Save it to a temporary buffer.
#     buf = BytesIO()
#     print("buf", buf)
#     fig.savefig(buf, format="png", dpi=100)
#     print(fig)
#     # Embed the result in the html output.
#     data = base64.b64encode(buf.getbuffer()).decode("ascii")
#     print("data", data)

#     return f"<img src='data:image/png;base64,{data}'/>"

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