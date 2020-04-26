# 贴吧爬虫
# '生活大爆炸'
import requests
from bs4 import BeautifulSoup
import time
import sys

def getHTMLText(url) :

	try :
		r = requests.get(url,timeout = 30)
		r.raise_for_status()
		# r.encoding = r.apparent_encoding
		r.encoding = 'utf-8'
		return r.text
	except:
		return ''

def parserHTML(html, ulist, autor, recordTime):

	soup = BeautifulSoup(html,'html.parser')
	# 搜索所有标题
	liTags = soup.findAll('li', attrs={'class':'j_thread_list clearfix'})
	# 遍历所有带有 li 标签
	for li in liTags :
		# ^标题
		# 寻找a 标签下的标题栏
		ulist.append(li.find('a', attrs ={'rel':'noreferrer'}).text.strip())
		# ^作者
		# 在li 标签下 继续寻找作者->进行分割
		autor.append(li.find('span',attrs={'class':'tb_icon_author'})['title'].split(':')[1])
		# ^最后回复时间
		# 在li 标签下寻找
		recordTime.append(li.find('span', attrs={'class':'threadlist_reply_date pull_right j_reply_data'}).text.strip())



def printText(ulist, autor, recordTime):

	#写入文件
	try :
		# 写入自己的想要存的地址
		handle = open('baidutieba.txt', 'w')
		#
		# ver1 : 把标题和作者导入txt文件里
		# ver2 : 1.加入最后发帖时间 最后回复人 
		#	     2.添加 'prograss bar'增加用户体验
		#	     3.调整文件观看舒适度 1.0v			  
		#		 4.重新设置网站链接 无cookies 登录

		# 文件所属长度
		# 199
		file_len = len(ulist)

		# i == (0 ~ 199)
		# +1 防止 到达 99% 停止
		for i in range(file_len + 1):
		
			time.sleep(0.1)
			percent = float(i) / float(file_len)
			sys.stdout.write("\r正在写入: [{0:50}] {1:.1f}%".format('#' * int(percent * 100 / 2 ), percent * 100))
			sys.stdout.flush()

			if i == file_len :
				pass 
			# handle.write(ulist[i] + '\t\t' + autor[i] + '\n')
			handle.write('标题: {} \t 作者: {} \t 最后回复时间: {} \n'.format(ulist[i], autor[i], recordTime[i]))

		handle.close()

	except:
		'ERRO'

def main():

	url_star = 'https://tieba.baidu.com/f?ie=utf-8&kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&fr=search'

	# 设定页面范围的所有标题
	titleInfo = []
	# 设定页面范围的所有话题的作者
	autorInfo = []
	# 设定页面范围的所有话题的最后回复时间
	lastTime = []

	for i in range(4) :
		url = url_star + '&pn=' + str(i*50)
		html = getHTMLText(url)
		parserHTML(html,titleInfo,autorInfo,lastTime)

	printText(titleInfo, autorInfo,lastTime)

main()



