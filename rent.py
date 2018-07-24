import requests
import datetime
import sys
import re

html = "<html>"
day_dict = dict([(1, 31), (2, 28), (3, 31), (4, 30), (5, 31), (6, 30),
				(7, 31), (8, 31), (9, 30), (10, 31), (11, 30), (12, 31)])

def validDate(y, m, wd):
	days = []
	global day_dict
	for d in range(1, day_dict[m] + 1):
		if datetime.date(y, m, d).isoweekday() == wd:
			days.append(d)
	return days


def draw_table(date):
	global html
	base_url = "https://pe.ntu.edu.tw/api/rent/yearuserrent"
	param = {
		'rentDateS' : date,
		'rentDateE' : date
	}
	r = requests.get(base_url, params=param)
	
	if r.status_code == requests.codes.ok:
		print(date + '  searching...')
	else:
		print(date + '  fail')

	table = {}
	for i in range(4, 8):
		table['排球場('+str(i)+')'] = {"08:00~10:00":[], "10:00~12:00":[], "12:00~13:00":[], "13:00~15:00":[], "15:00~17:00":[], "17:00~18:00":[], "18:00~20:00":[], "20:00~22:00":[]}

	global success
	for i in r.json():
		try:
			if success:	# 欲查詢抽籤結果
				if i['waitConfirmTime'] and i['statusRent'] != 3:	# 被抽中 & 沒取消
					table[i['venueName']][i['rentTimePeriod']].append(i['yearUserUnitName'])
			else:		# 欲查詢放籤情形
				table[i['venueName']][i['rentTimePeriod']].append(i['yearUserUnitName'])
		except:
			pass
		try:	# 體育組事先登記
			if i['statusRent'] == 1:
				table[i['venueName']][i['rentTimePeriod']].append(i['unitName'])
		except:
			pass

	html += "<tr><th>日期 \ 時段</th><th>排球場(4)</th><th>排球場(5)</th><th>排球場(6)</th><th>排球場(7)</th></tr>"
	for time in table['排球場(4)']:
		html += "<tr><td>{}</td>".format(time)
		for state in '排球場(4)', '排球場(5)', '排球場(6)', '排球場(7)':
			html += "<td>{}</td>".format('<br>'.join(f for f in table[state][time]))
		html += "</tr>"
	html += "</table>"
	

day = ['', '一', '二', '三', '四', '五', '六', '日']

success = int(input('欲查詢放籤情形請輸入 0 / 欲查詢抽籤結果請輸入 1: '))
if success not in range(0, 2):
	sys.exit()
y = int(input('年 (範圍：2018 - 2100): '))
if y not in range(2018, 2101):
	sys.exit()
m = int(input('月 (範圍：1 - 12): '))
if m not in range(1, 13):
	sys.exit()
choose = int(input('以星期查詢請輸入 0 / 以日期查詢請輸入 1: '))
if choose not in range(0, 2):
	sys.exit()

while True:
	days = []
	if choose == 0:
		query = input('星期 (範圍：1 - 7): ')
		if not re.match(re.compile(r'[1-7]$'), query):
			break
		wd = int(query)
		days = validDate(y, m, wd)
		
	else:
		query = input('日期 (範圍：1 - %d): ' % day_dict[m])
		if not query.isdigit() or int(query) > day_dict[m] or int(query) < 1:
			break
		days.append(int(query))
	
	for d in days:
		date = "{}-{}-{}".format(y, "%02d"%m, "%02d"%d)
		wd = datetime.date(y, m, d).isoweekday()
		html += """<h4>{}</h4><table border="1">""".format(date+' ('+day[wd]+')')
		draw_table(date)


html += "</html>"
file = open("rent.html", "w")
file.write(html)
file.close()
print("result write to file rent.html")