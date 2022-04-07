import logging
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


@app.route('/')
@app.route('/selectServer', methods=['GET'])
def home():
    """The main landing page of the site.
    This is where the user enters which server address they are using.
    """

    return render_template('selectServer.html')


@app.errorhandler(500)
def server_error(error):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


@app.errorhandler(404)
def page_not_found(error):
    logging.warning('Missing page requested')
    return render_template('404.html'), 404


if __name__ == '__main__':
    # Only run for local development.
    app.run(host='127.0.0.1', port=8080, debug=True)
