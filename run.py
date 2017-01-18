from flask import Flask, render_template, send_from_directory
from flask_restful import Api

from resources import BookListResource, CategoriesListResource, WbookListResource, WbookResource, WuserResource

app = Flask(__name__, static_folder='templates/static')
api = Api(app)


@app.route('/<path:filename>')
def file(filename):
    from os import path
    return send_from_directory(path.join(app.root_path, 'templates'), filename)


@app.route('/')
def index():
    return render_template('index.html')


api.add_resource(BookListResource, '/api/v1/book', endpoint='books')
api.add_resource(CategoriesListResource, '/api/v1/category', endpoint='categories')
api.add_resource(WbookListResource, '/api/v1/bookwbook', endpoint='wbooks')
api.add_resource(WbookResource, '/api/v1/wunderlist/book', endpoint='wbook')
api.add_resource(WuserResource, '/api/v1/wunderlist/user', endpoint='wuser')


if __name__ == '__main__':
    app.run(debug=True)
