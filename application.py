from app.views import app

from app.predict import predict_bp
from app.comment import comment_bp
from app.download import download_bp

app.register_blueprint(predict_bp, url_prefix="/predict")
app.register_blueprint(comment_bp, url_prefix="/comment")
app.register_blueprint(download_bp, url_prefix="/download")

if __name__ == "__main__":
    app.run(debug=True)