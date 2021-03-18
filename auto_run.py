import tweet_api
import schedule,time,datetime

def job():
	now = datetime.datetime.now()
	print(now.strftime('%Y-%m-%d %H:%M:%S'))
	tweet_api.main()

# ３分おきに実行
schedule.every(3).minutes.do(job)

while True:
	schedule.run_pending()
	time.sleep(10)
