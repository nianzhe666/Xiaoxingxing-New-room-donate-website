from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "你的 Flask 项目部署成功了！"

if __name__ == '__main__':
    app.run()
