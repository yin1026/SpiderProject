# 豆瓣抓取电影top 250

import requests
from bs4 import BeautifulSoup
import time
import sys

# 取得网页内容
def getHTMLText(url):
	user = {'user-agent':'Mozilla/5.0'}
	try:
		r = requests.get(url,headers = user)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return ''

# 把摘出来的内容放在列表里
def parserHTML(html,title,rating_num,rank,quote):

	soup = BeautifulSoup(html, 'html.parser')

	# 电影名字
	Tages = soup.findAll('div', attrs = {'class':'hd'})
	for tag in Tages: 
		title.append(tag.find('span', attrs = {'class':'title'}).text)
	# 电影评分
	ruting_num_tages = soup.findAll('div',attrs = {'class':'star'})
	for ruting_num_tag in ruting_num_tages:
		rating_num.append(ruting_num_tag.find('span', attrs = {'class':'rating_num'}).text)
	# 电影排名
	rank_tages = soup.findAll('div', attrs = {'class':'pic'})
	for rank_tag in rank_tages :
		rank.append(rank_tag.find('em').text)
	# 电影短评
	quote_tages = soup.findAll('p', attrs = {'class':'quote'})
	for quote_tag in quote_tages:	
		quote.append(quote_tag.find('span',attrs = {'class':'inq'}).text)


def fileSys(title,rating_num,rank,quote):

	#写入文件
	try :
		# 写入自己的想要存的地址
		# /Users/作者/
		handle = open('/Users/yinjunhong/spiderProject/doubanMovie.txt', 'w')

		file_len = len(title)

		# tite 250
		# i == (0 ~ 250)
		# +1 防止 到达 99% 停止
		for i in range(0, file_len + 1):

			time.sleep(0.1)
			percent = float(i) / float(file_len)
			sys.stdout.write("\r正在写入: [{0:50}] {1:.1f}%".format('#' * int(percent * 100 / 2 ), percent * 100))
			sys.stdout.flush()

			if i == file_len :
				pass
			else :
				# 有些电影没有评价 程序意外处理需要！！！
				# 从搜索开始 except!
				handle.write('排名: {} \t 电影名字: {} \t\t 评分: {} \t \n'.format(rank[i], title[i], rating_num[i]))

		handle.close()

	except:
		'ERRO'

def main():
	# 电影名字
	title = []
	# 评分
	rating_num = []
	# 排名
	rank = []
	# 简单的简评
	quote = []

	page: int = 0

	while page <= 225 :
		url = 'https://movie.douban.com/top250?start=' + str(page) + '&filter='
		
		html = getHTMLText(url)

		parserHTML(html,title,rating_num,rank,quote)

		page += 25

	fileSys(title,rating_num,rank,quote)

main()











