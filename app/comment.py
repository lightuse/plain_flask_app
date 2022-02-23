from flask import request, render_template, current_app
import os
from flask import Blueprint
from app.model import Comment

comment_bp = Blueprint("comment", __name__, url_prefix="/comment")

@comment_bp.route("/", methods=['POST'])
def comment():
    # コメントの設定
    commenter_num = request.form['commenterNum']
    commenter_index = int(commenter_num)
    subject_index = int(request.cookies.get('result_index', None))

    comment = Comment(commenter_index, subject_index)
    comment_author = comment.commenter_name()
    comment_message = comment.message()

    # スタンプアイコンをランダムで決定
    import random
    stamp_index = str(random.randint(0, 3))
    stamp_name = 'stamp/stamp_' + stamp_index + '.png'

    # 画像読み込み
    filename = request.cookies.get('filename', None)

    img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    stamp_icon_path = os.path.join(current_app.config['IMAGE_FOLDER'], stamp_name)
    stamp_logo_path = os.path.join(current_app.config['IMAGE_FOLDER'], 'stamp/murin_an_logo.png')
    line_vertical_path = os.path.join(current_app.config['IMAGE_FOLDER'], 'stamp/vertical.png')
    line_horizontal_path = os.path.join(current_app.config['IMAGE_FOLDER'], 'stamp/horizontal.png')

    from PIL import Image
    try:
        bg_img = Image.open(img_path)
        # exif情報取得
        exifinfo = bg_img._getexif()
        # exif情報からOrientationの取得
        orientation = exifinfo.get(0x112, 1)
        # 画像を回転
        bg_img = rotateImage(bg_img, orientation)
    except:
        pass

    stamp_icon = Image.open(stamp_icon_path)
    stamp_logo = Image.open(stamp_logo_path)
    line_horizontal = Image.open(line_horizontal_path)
    line_vertical = Image.open(line_vertical_path)

    # スタンプサイズ調整
    img_w, img_h = bg_img.size
    icon_w, icon_h = stamp_icon.size
    logo_w, logo_h = stamp_logo.size
    horizontal_w, _ = line_horizontal.size
    _, vertical_h = line_vertical.size

    icon_ratio = img_w * 0.15 / icon_w
    icon_w = int(icon_w * icon_ratio)
    icon_h = int(icon_h * icon_ratio)

    logo_ratio = icon_w / logo_w
    logo_w = int(logo_w * logo_ratio)
    logo_h = int(logo_h * logo_ratio)

    margin = int(img_w * 0.01) 
    horizontal_w = int(img_w - margin * 2)
    vertical_h = int(img_h - margin * 2)
    stroke = int(img_w * 0.004)

    stamp_icon = stamp_icon.resize(size=(icon_w,icon_h))
    stamp_logo = stamp_logo.resize(size=(logo_w,logo_h)) 
    if stroke <= 0:
        stroke = 1
    line_horizontal = line_horizontal.resize(size=(horizontal_w,stroke))
    line_vertical = line_vertical.resize(size=(stroke,vertical_h))

    # スタンプ貼り付け位置定義
    position_icon = (margin * 4,margin * 4)
    position_logo = (margin * 4,margin * 4 + icon_h + margin)
    position_horizontal_top = (margin,margin * 2)
    position_horizontal_down = (margin,img_h-margin*2)
    position_vertical_left = (margin*2,margin)
    position_vertical_right = (img_w-margin*2,margin)

    # スタンプ貼り付け
    bg_img.paste(stamp_icon, position_icon, stamp_icon)
    bg_img.paste(stamp_logo, position_logo, stamp_logo)
    bg_img.paste(line_horizontal, position_horizontal_top, line_horizontal)
    bg_img.paste(line_horizontal, position_horizontal_down, line_horizontal)
    bg_img.paste(line_vertical, position_vertical_left, line_vertical)
    bg_img.paste(line_vertical, position_vertical_right, line_vertical)

    # 加工済み画像保存
    stamped_img_name = "stamped_" + filename
    bg_img.save(os.path.join(current_app.config['UPLOAD_FOLDER'], stamped_img_name))

    recommend_img_path = '/static/images/recommend_image.jpeg'
    return render_template("comment.html",
                            stamped_img_name = stamped_img_name, 
                            comment_author = comment_author, 
                            comment_message = comment_message,
                            recommend_img_path = recommend_img_path,
                            )

def rotateImage(img, orientation):
    from PIL import Image
    # orientationの値に応じて画像を回転させる
    if orientation == 1:
        pass
    elif orientation == 2:
        # 左右反転
        img_rotate = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation == 3:
        # 180度回転
        img_rotate = img.transpose(Image.ROTATE_180)
    elif orientation == 4:
        # 上下反転
        img_rotate = img.transpose(Image.FLIP_TOP_BOTTOM)
    elif orientation == 5:
        # 左右反転して90度回転
        img_rotate = img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90)
    elif orientation == 6:
        # 270度回転
        img_rotate = img.transpose(Image.ROTATE_270)
    elif orientation == 7:
        # 左右反転して270度回転
        img_rotate = img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270)
    elif orientation == 8:
        # 90度回転
        img_rotate = img.transpose(Image.ROTATE_90)
    else:
        pass

    return img_rotate