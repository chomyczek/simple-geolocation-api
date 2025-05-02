from flask import Flask

from route import index, add, show, delete

app = Flask(__name__)

app.add_url_rule('/', view_func=index.index)
app.add_url_rule('/add', methods=["POST"], view_func=add.add)
app.add_url_rule('/show', methods=["POST"], view_func=show.show)
app.add_url_rule('/delete', methods=["POST"], view_func=delete.delete)

# todo Remove
app.run()
