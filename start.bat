cd D:\Dev\Alternance\IA\TP\Sujet04-Movies
CALL env\Scripts\activate

set FLASK_APP=run.py
set FLASK_ENV=development

START http://127.0.0.1:5000/home

flask run
