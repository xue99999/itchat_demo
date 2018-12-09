import re
import itchat
from pyecharts import Page, Pie, Bar, Map

def get_key_info(friends_info, key):
    return list(map(lambda friend_info: friend_info.get(key), friends_info))

def get_friends_info(friends):
    friends_info = dict(
        username=get_key_info(friends, "UserName"),
        sex=get_key_info(friends, "Sex"),
        province=get_key_info(friends, "Province"),
        city=get_key_info(friends, "City")
    )
    return friends_info


def count_nums(new_list):
    new_dict = {}
    for i in new_list:
        if bool(re.search('[a-z]|[A-Z]', i)):
            continue
        elif not new_dict.__contains__(i):
            new_dict[i] = 1
        else:
            new_dict[i] += 1
    new_dict.pop('')
    return new_dict


def analysis(friends):
    friends_info = get_friends_info(friends)

    # 性别图
    sex_list = friends_info['sex']
    from collections import Counter
    sex_dict = dict(Counter(sex_list))
    attr = ['未知', '男性', '女性']
    value = [sex_dict[0], sex_dict[1], sex_dict[2]]
    page = Page()
    chart1 = Pie("微信好友性别比例图", title_pos='center')
    chart1.add("", attr, value, is_label_show=True, legend_orient="vertical", legend_pos="left")
    page.add(chart1)

    # 省份图
    province_list = friends_info['province']
    print(province_list)
    province_dict = count_nums(province_list)
    attr, value = list(province_dict.keys()), list(province_dict.values())
    chart2 = Map('好友省级分布(中国地图)', width=1200, height=600)
    chart2.add('', attr, value, maptype='china', is_label_show=True, is_visualmap=True, visual_text_color='#000')
    page.add(chart2)

    # 中国城市分析图
    city_list = friends_info['city']
    city_dict = count_nums(city_list)
    print('city------------')
    print(city_dict)
    top_ten_city = dict(sorted(city_dict.items(), key=lambda x: x[1], reverse=True)[0:10])
    print('---------------')
    print(top_ten_city)
    print('---------------')
    attr, value = list(top_ten_city.keys()), list(top_ten_city.values())
    chart3 = Bar('好友城市分布Top10柱状图', width=900, height=500)
    chart3.add('', attr, value, is_stack=False, is_label_show=True, bar_category_gap='20%')
    page.add(chart3)

    page.render('analysisResult.html')



if __name__ == '__main__':
    itchat.auto_login()
    friends = itchat.get_friends()
    print(friends)

    analysis(friends)


