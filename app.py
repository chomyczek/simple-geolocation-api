from flask import Flask

from route import add, delete, index, get
from util import app_config
from util.db_handler import DbHandler

app = Flask(__name__)

app.add_url_rule("/", view_func=index.index)
app.add_url_rule("/add", methods=["POST"], view_func=add.add)
app.add_url_rule("/get", methods=["POST"], view_func=get.get)
app.add_url_rule("/delete", methods=["POST"], view_func=delete.delete)


if __name__ == "__main__":
    app_config.set_db_url()
    app_config.set_token("test")  # todo
    DbHandler().prepare_db_tables()
    app.run()
