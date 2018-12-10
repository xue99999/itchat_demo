import os, random, math
from PIL import Image
import itchat

def get_key_info(friends_info, key):
    return list(map(lambda friend_info: friend_info.get(key), friends_info))

def get_friends_info(friends):
    friends_info = dict(
        username=get_key_info(friends, 'UserName'),
    )
    return friends_info

def get_head_img(friends):
    friends_info = get_friends_info(friends)
    username = friends_info['username']

    for i, uname in enumerate(username):
        with open("headImgs/" + str(i) + ".png", "wb") as f:
            img = itchat.get_head_img(uname)
            f.write(img)


def create_img():
    x = 0
    y = 0
    imgs = os.listdir("headImgs")
    random.shuffle(imgs)

    input_length = int(input("请输入手机屏保长的像素值(一般是两个值中较大的值):"))
    input_width = int(input("请输入手机屏保宽的像素值(一般是两个值中较小的值):"))

    new_img = Image.new('RGBA', (input_width, input_length))
    width = int(math.sqrt(input_length * input_width / len(imgs)))
    num_line = int(input_width / width)

    for i in imgs:
        try:
            img = Image.open('headImgs/' + i)
        except IOError:
            print("第{}张图片为空".format(i))
        else:
            img = img.resize((width, width), Image.ANTIALIAS)
            new_img.paste(img, (x * width, y * width))

            x += 1
            if x > num_line:
                x = 0
                y += 1


    new_img.save("mixedImg.png")
    itchat.send_image('mixedImg.png', toUserName='filehelper')


if __name__ == '__main__':
    itchat.auto_login()
    friends = itchat.get_friends()
#    生成最终的图片
#    create_img()
#    获取微信好友的头像
    get_head_img(friends)
