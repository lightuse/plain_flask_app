from flask import request, send_file
from flask import Blueprint

download_bp = Blueprint("download", __name__, url_prefix="/download")

@download_bp.route("/", methods=["GET"])
def download():
    filename = request.cookies.get('filename', None)
    stamped_img_name = "stamped_" + filename
    filepath = 'static/uploads/' + stamped_img_name

    # 画像保存時に付けたプレフィックスをファイル名から削除
    idx = filename.find('_')
    imgname = filename[idx+len('_'):]
    imgname = "stamped_" + imgname

    return send_file(filepath, as_attachment=True,
                     attachment_filename=imgname,
                     mimetype='image/jpeg')

