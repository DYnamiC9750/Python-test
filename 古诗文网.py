
import requests
from lxml import etree
import pytesseract
from PIL import Image


def discern(imgLink):
    n = 0
    image = Image.open(imgLink)
    result = pytesseract.image_to_string(image)
    while result == '':  # 有几率失败
        n += 1
        result = pytesseract.image_to_string(image)  # 存放识别结果
        if(n > 50):  # 如果失败次数大于50就取消
            print("识别失败！")
            break
    result = result.replace('\n', '')
    print(result)
    return result


def denglu():  # 登录古诗文网
    global n
    if(n > 10):
        print("失败次数太多！停止")
        return
    flag = 1
    if flag != 1:
        return
    url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
    }
    session = requests.Session()
    html_str = session.get(url=url, headers=header).text
    tree = etree.HTML(html_str)
    i = tree.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
    img = tree.xpath('//*[@id="imgCode"]/@src')[0]
    img_url = 'https://so.gushiwen.cn'+img
    img_data = session.get(url=img_url, headers=header).content
    with open('验证码图片1.jpg', 'wb')as fp:
        fp.write(img_data)  # 加载验证码图片到达本地
    code = discern('验证码图片1.jpg')  # 识别验证码并返回
    post_url = 'https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx'
    data_loadd = {
        '__VIEWSTATE': i,
        '__VIEWSTATEGENERATOR': 'C93BE1AE',
        'from': 'http://so.gushiwen.cn/user/collect.aspx',
        'email': '1319341631@qq.com',
        'pwd': '135790iop0',
        'code': code,
        'denglu': '登录'
    }
    denglu_html = session.post(
        url=post_url, data=data_loadd, headers=header)
    denglu_html_str = denglu_html.text
    tree_real = etree.HTML(denglu_html_str)
    p = tree_real.xpath('//*[@id="aspnetForm"]/div[3]/span/b/text()')
    n += 1
    flag = p.count("快捷登录古诗文网")
    if (flag == 1):
        print("失败一次")
        denglu()
    else:
        print("成功！")
        with open('登录古诗文网.html', 'w', encoding='utf-8')as fp:
            fp.write(denglu_html_str)


n = 0
denglu()
