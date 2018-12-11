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

    # 如果不存在该目录，就创建一个
    if not os.path.exists('headImgs'):
        os.mkdir('headImgs')

    for i, uname in enumerate(username):
        # 如果是最后一张图片，就创建一张合成的图片
        with open("headImgs/" + str(i) + ".png", "wb") as f:
            img = itchat.get_head_img(uname)
            f.write(img)



def create_img():
    x = 0
    y = 0
    imgs = os.listdir("headImgs")
    # 随机打乱序列或者元祖
    random.shuffle(imgs)

    input_length = int(input("请输入手机屏保长的像素值(一般是两个值中较大的值):"))
    input_width = int(input("请输入手机屏保宽的像素值(一般是两个值中较小的值):"))

    # 生成一张输入宽高相等的底图
    new_img = Image.new('RGBA', (input_width, input_length))
    # 微信头像采用正方形图片, 头像宽 * 头像高 * 所有的小正方形头像 = 输入的手机宽高
    width = int(math.sqrt(input_length * input_width / len(imgs)))
    # 每行有多少个图片, 用手机宽度 / 每张头像的宽度就行
    num_line = int(input_width / width)

    for i in imgs:
        try:
            img = Image.open('headImgs/' + i)
        except IOError:
            print("第{}张图片为空".format(i))
        else:
            # 缩放图片到指定的宽高，Image.ANTIALIAS代表高质量图片
            img = img.resize((width, width), Image.ANTIALIAS)
            # paset 拼接图片, 后面的参数是x轴和y轴的位置
            new_img.paste(img, (x * width, y * width))

            # 正常情况下，x轴往右一个格，x大于一行能放的图片数之后，y轴往下移一个格
            x += 1
            if x > num_line:
                x = 0
                y += 1


    new_img.save("mixedImg.png")
    itchat.send_image('mixedImg.png', toUserName='filehelper')


if __name__ == '__main__':
    itchat.auto_login()
    friends = itchat.get_friends()

#    获取微信好友的头像
#    get_head_img(friends)
#    合成微信好友屏保图
    create_img()
