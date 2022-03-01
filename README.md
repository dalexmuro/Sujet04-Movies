# Flask  & Etude d'un dataset 

Vous allez mettre en place une petite application pour afficher votre analyse de données à l'aide de Flask.

Vous êtes libre d'analyser le dataset de votre choix.

Vous avez 6 semaines avant de rendre votre étude.

Le projet théoriquement ne doit pas vous prendre plus de 2 jours.

## Contraintes & remarques

- Utilisez Pandas, de la dataviz, ...

- Utilisez Flask pour la partie application Web qui présentera votre travail.

- Vous travaillez par équipe (2 à 3 personnes max).

- L'application peut consommer une/des API(s) de données.

- L'utilisation d'une base de données n'est pas exigée, vous pouvez cependant en utiliser (dans ce cas repportez vous sur les remarques plus bas pour la mettre en place ).

- Vous devez avant de commencer votre développement résumer l'étude que vous souhaitez réaliser sur votre/vos datasets.

- Votre travail devra être accessible sur un dépôt Git.

## Environement de travail

Nous allons installer un environement virtuel de travail dans lequel nous allons installer flask avec pip.

Attention dans un environement virtualisé (dans le dossier, voir plus bas) si vous utilisez Git vous devez créer un fichier .gitignore afin de ne pas versionner le dossier de virtualisation :

### Fichier .gitignore

```txt

/env

```

L'utilisation d'un environement virtualisé est courant, il permet de ne pas installer des dépendances sur la machine et facilite le travail entre développpeur.

```bash
# vérifier que virtualenv est bien installé.
pip install virtualenv

# puis dans le dossier de travail

virtualenv -p python3 env

# Vous pouvez également changer le nom du dossier env

virtualenv -p python3 env2

```

Chaque virtualisation est installée dans un dossier et est propre à celui-ci.

Cette commande crée un dossier env dans lequel on utilise Python3. Pour activer l'environement il faudra taper la commande suivante :

```bash
# sous Mac et Linux
source env/bin/activate

# Dans cmder pour Windows
.\\Scripts\\activate.bat

```

En utilisant la commande which ou where pour Windows vous pouvez constater que le chemin de l'exécutable Python n'est plus le même, il correspond à l'environement que vous venez de créer.

```bash

# Mac ou Linux
which python
# Windows
where python

```

Attention, pour chaque session de votre console vous devez lancer l'environement pour l'activer.

Pour désactiver et supprimer l'environement tapez la commande suivante :

```bash

# Mac ou Linux
deactivate

# Dans cmder pour Windows
.\\Scripts\\deactivate.bat

# Suppression du dossier d'environement
rm -rf env

# Pour désactiver l'environement
deactivate

# Dans cmder pour Windows
.\\Scripts\\deactivate.bat

```

### Création d'un fichier de dépendance

Afin de préciser les dépendances utilisées dans votre projet vous devez créer le fichier suivant, cela permettra de partager vos projets et de les migrer facilement sur un autre poste de travail.

Rentrez dans votre environement virtualisé avant !

```bash

# sous Mac et Linux
source env/bin/activate
.\\Scripts\\activate.bat

# commande permettant d'écrire les dépendances dans ce fichier avec leurs versions.
pip freeze > requirements.txt

# Sous Windows
pip list > requirements.txt

```

### Installation de Flask

Une fois l'environement démarré installer Flask dans ce dernier dans un dossier "flaskapp"

```python
source env/bin/activate
# Sous Windows
# .\Scripts\activate.bat

(env) flaskapp pip install flask

```

### Organisation des dossiers

- Un dossier "static" pour les assets.
- Un dossier "templates" pour les vues.
- Un dossier "tests" pour les tests.

Créez également le fichier **run.py**, il permettra d'initialiser et lancer l'application.

Ajoutez les lignes suivantes dans le fichier run.py :

```python
from flask import Flask, session, redirect, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello world !"

if __name__ == "__main__":
    app.run(debug=True)
```

Puis en console :

```bash
# Windows
set FLASK_APP=run.py

# Mac ou Linux
export FLASK_APP=run.py
export FLASK_ENV=development

# Windows
set FLASK_ENV=development

# Lancer Flask
flask run
```

## Modèle Titanic

Vous pouvez si vous le souhaitez créer un modèle afin d'enregistrer en session par exemple une analyse spécifique, nous vous donnons ci-dessous un exemple

```python


class Titanic(db.Model):
   
    def __init__(self, passengerId, name, survived, sex, age, fare):
        self.passengerId = passengerId
        self.name        = name
        self.survived    = survived
        self.sex         = sex
        self.age         = age
        self.fare        = fare


def init_db():
    
    lg.warning('Serialize data')

# création d'un décorateur permettant de définir une commande CLI

@app.cli.command()
def init():
    session['titanic'] = Titanic(passengerId, name, survived, sex, age, fare)

```

Pour lancer ce code tapez maintenant en ligne de commande :

```bash
# Permet de lister les commandes accessibles
flask

# Puis pour initialiser les données par rapport au nom de votre décorateur
flask init

```

Vous pouvez interagir directement avec les objets du projet dans la console :

```bash
# La console Flask
flask shell
>>> from run import db, User

# vérifier que les données sont bien créées :
>>> titanic = Titanic(1, "name", 1, "female", age, fare)

```

## Mise en place des vues

Dans le dossier templates créer les deux fichiers suivants :

index.html et base.html

Le fichier base.html permet de créer un template de "base" qu'hérieront les autres vues composites :

```html
<!DOCTYPE html>
<title>{% block title %}{% endblock %} - Flaskr</title>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" />
<nav>
  <h1>Flaskr</h1>
  <ul></ul>
</nav>
<section class="content">
  <header>{% block header %}{% endblock %}</header>

  {% block content %}{% endblock %}
</section>
```

La vue index.html héritera de la vue base.html

```html
{% extends 'base.html' %} {% block header %}
<h1>Hello Flask</h1>
{% endblock %} {% block content %}
<ul class="users"></ul>
{% endblock %}
```

## Passer les données à la vue

Flask possède un moteur de rendu ou templating, la méthode render_template permet d'injecter des données à la vue ou template :

```python

from flask import Flask, render_template

@app.route("/")
def hello():
    users = User.query.all()
    return render_template('index.html', users=users)

```

Essayez d'afficher maintenant les donnes dans la vue, pensez à lancer le serveur à l'aide de la commande suivante :

```bash
flask run
```

## Traitement des formulaires

```python
@app.route('/send', methods=['GET', 'POST'])
def send():
    return '''
              <form method="POST">
                  <div><label>Sex: <input type="text" name="sex"></label></div>
                  <div><label>pClass: <input type="text" name="pclass"></label></div>
                  <input type="submit" value="Submit">
              </form>'''

```

Pour recevoir et traiter les données vous utiliserez la méthode request de Flask comme suit :

```python
if request.method == 'POST':
        language = request.form.get('sex')
        framework = request.form.get('pclass')
        return f'''
                  <h1>The sex value is: {sex}</h1>
                  <h1>The class value is: {pclass}</h1>'''
```

## Afficher une image dans une page

Attention vous devez importez les dépendances suivantes :

```python
import base64
from io import BytesIO
from matplotlib.figure import Figure
``` 

Voici une route qui affichera une droite. Vous pouvez également passer ce graphique à vos vues.

```python
@app.route("/line")
def hello():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return f"<img src='data:image/png;base64,{data}'/>"
```

## Application

Prennez un dataset de votre choix et analysez le en affichant les résultats dans des pages Web.

Créez un formulaire pour rendre intéractif les options de votre analyse.
