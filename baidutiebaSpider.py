# 贴吧爬虫
# '生活大爆炸'
import requests
from bs4 import BeautifulSoup
import time

def getHTMLText(url) :

	try :
		r = requests.get(url,timeout = 30)
		r.raise_for_status()
		# r.encoding = r.apparent_encoding
		r.encoding = 'utf-8'
		return r.text
	except:
		return ''

def parserHTML(html, ulist, autor):

	soup = BeautifulSoup(html,'html.parser')
	# 搜索所有标题
	liTags = soup.findAll('li', attrs={'class':'j_thread_list clearfix'})
	# 遍历所有带有 li 标签
	for li in liTags :
		# 标题
		# 寻找a 标签下的标题栏
		ulist.append(li.find('a', attrs ={'rel':'noreferrer'}).text.strip())
		# 作者
		# 在li 标签下 继续寻找作者->进行分割
		autor.append(li.find('span',attrs={'class':'tb_icon_author'})['title'].split(':')[1])

	# text 1 : autor 是否准确
	# print(autor)

def printText(ulist, autor):

	#写入文件
	try :
		# 写入自己的想要存的地址
		handle = open('baidutieba.txt', 'w')

		# 把标题和作者导入txt文件里
		for i in range(len(ulist)):
			handle.write(ulist[i] + '\t\t' + autor[i] + '\n')
		handle.close()

	except:
		'ERRO'

def main():

	url_star = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8'

	# 设定页面范围的所有标题
	titleInfo = []
	# 设定页面范围的所有话题的作者
	autorInfo = []

	for i in range(4) :
		url = url_star + '&pn=' + str(i*50)
		html = getHTMLText(url)
		parserHTML(html,titleInfo,autorInfo)

	printText(titleInfo, autorInfo)

main()



