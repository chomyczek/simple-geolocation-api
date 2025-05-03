from flask import Flask

from route import add, delete, index, show

app = Flask(__name__)

app.add_url_rule("/", view_func=index.index)
app.add_url_rule("/add", methods=["POST"], view_func=add.add)
app.add_url_rule("/show", methods=["POST"], view_func=show.show)
app.add_url_rule("/delete", methods=["POST"], view_func=delete.delete)

# if not token:
#     raise ValueError("Token for ipstack.com is not provided")

# todo Remove
app.run()
