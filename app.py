from flask import Flask

from route import add, delete, index, show
from util import app_config
from util.db_handler import DbHandler

app = Flask(__name__)

app.add_url_rule("/", view_func=index.index)
app.add_url_rule("/add", methods=["POST"], view_func=add.add)
app.add_url_rule("/show", methods=["POST"], view_func=show.show)
app.add_url_rule("/delete", methods=["POST"], view_func=delete.delete)

# todo verify token

if __name__ == "__main__":
    app_config.set_db_url()
    # todo prepare db on demand
    DbHandler().prepare_db_tables()
    app.run()
