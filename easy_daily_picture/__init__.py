import logging
import os
from logging import handlers

from flask import Flask, has_request_context, request


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_CONNECT='mysql+mysqlconnector://stock:sdasdd@22.125.343.44:3306/stock?charset=utf8',
        DB_POOL_SIZE=10,
        DB_POOL_RECYCLE=3600
    )

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    ################################################################################################
    # 创建存储图片的目录
    app.image_dir = os.path.join(app.instance_path, app.config['IMAGE_DIR'])
    try:
        os.makedirs(os.path.join(app.instance_path, app.config['IMAGE_DIR']))
    except OSError as e:
        pass
    ################################################################################################
    # 数据库

    from .util.util_base import db
    db_session_maker = db.create_db_session_maker(app.config['DB_CONNECT'], app.config['DB_POOL_SIZE'], app.config['DB_POOL_RECYCLE'])
    app.db_session_maker = db_session_maker

    from .util.util_base import db
    db.release_connection_when_request_end(app)

    ################################################################################################
    # 蓝图
    from .views import future
    app.register_blueprint(future.bp)

    ################################################################################################
    # 日志
    # 在蓝图中使用 current_app 打印日志

    class RequestFormatter(logging.Formatter):
        def format(self, record):
            if has_request_context():
                record.url = request.url
                record.remote_addr = request.remote_addr

                record.params_get = request.args
                record.params_form = request.form
                record.params_json = request.get_json()

            else:
                record.url = None
                record.remote_addr = None
                record.params_get = None
                record.params_form = None
                record.params_json = None

            return super().format(record)

    formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s %(levelname)s in %(module)s: \n'
        'params_get:%(params_get)s\n'
        'params_form:%(params_form)s\n'
        'params_json:%(params_json)s\n'
        '%(message)s'
    )
    file_handler = handlers.RotatingFileHandler(os.path.join(app.instance_path, "../log/easy_daily_picture.log"), maxBytes=81920, encoding='utf-8', backupCount=9)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    try:
        os.makedirs(os.path.join(app.instance_path, "../log/easy_daily_picture.log"))
    except OSError:
        pass

    @app.after_request
    def add_cors(resp):
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    return app
