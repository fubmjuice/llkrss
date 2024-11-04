import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

# 用户的微博主页地址
USER_ID = '7884299354'  # 替换为目标用户的ID
WEIBO_URL = f'https://weibo.com/u/{USER_ID}'  # 构造用户主页URL

# 发起请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
response = requests.get(WEIBO_URL, headers=headers)

# 解析HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 创建RSS源
fg = FeedGenerator()
fg.id(WEIBO_URL)
fg.title(f'微博更新 - {USER_ID}')
fg.link(href=WEIBO_URL, rel='alternate')
fg.description(f'这是用户 {USER_ID} 的微博动态RSS源')

# 抓取微博内容
for post in soup.find_all('div', class_='WB_cardwrap'):
    # 提取微博文本
    title = post.find('div', class_='WB_text').get_text(strip=True)
    # 提取微博链接
    link = post.find('a', class_='S_txt1')['href']
    
    # 添加条目到RSS源
    entry = fg.add_entry()
    entry.id(link)
    entry.title(title)
    entry.link(href=link)
    entry.description(title)

# 生成RSS文件
rss_feed = fg.rss_str(pretty=True)
with open('weibo_rss.xml', 'wb') as f:
    f.write(rss_feed)

print("微博RSS源已生成，保存为weibo_rss.xml文件。")