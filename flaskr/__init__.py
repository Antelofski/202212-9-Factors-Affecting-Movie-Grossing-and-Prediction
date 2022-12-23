import os
from flask import Flask, request, render_template

import predict

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True,template_folder=tmpl_dir)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/prediction', methods=['GET', 'POST'])
    def prediction():
        if request.method == "POST":
            # getting input with name = fname in HTML form
            year = request.form['year']
            title = request.form['title']
            imdbRate = request.form['imdbRate']
            runtime = request.form['runtime']
            genres = request.form['genres']
            directors = request.form['directors']

            genres_list = genres.split(", ")
            directors_list = str(directors.split(", "))

            print(year + title + imdbRate + runtime)
            print(genres_list)
            print(directors_list)

            result = predict.predict(year, title, imdbRate, runtime, genres_list, directors_list)

            result = '{:,}'.format(int(result[0]))

            RESULT = "The predicted gross of your movie is $"+result

            print(result)
            return render_template("prediction.html", RESULT = RESULT)
            

        return render_template("prediction.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.secret_key = "super secret key"
    app.run(host='0.0.0.0', port=8111, debug=True)