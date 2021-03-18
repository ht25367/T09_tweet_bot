import settings,os
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import tweepy
import time

def set_driver(headless_flg=False):
	# Chromeドライバーの読み込み
	options = ChromeOptions()
	
	# ヘッドレスモード（画面非表示モード）の設定
	if headless_flg == True:
		options.add_argument('--headless')

	# 起動オプションの設定
	options.add_argument(
		'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
	# options.add_argument('log-level=3')
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--ignore-ssl-errors')
	options.add_argument('--incognito')		  # シークレットモードの設定を付与
	
	# ChromeのWebDriverオブジェクトを作成する。
	return Chrome(ChromeDriverManager().install(), options=options)
	# os.chdir( os.path.dirname(os.path.abspath(__file__)) )
	# return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

class Item:
	def __init__(self,name,url,quantity=0,stock_flg=False):
		self.name = name
		self.url = url
		self.quantity = quantity
		self.stock_flg = stock_flg
	
class Stock_Check:
	def __init__(self):
		self.item_list = []

	# チェック対象商品を .csv から読み込み
	def read_item_csv(self,file_name):
		item_csv = pd.read_csv(file_name)
		for i,row in item_csv.iterrows():
			self.item_list.append(Item(row[1],row[2],row[3],row[4]))
	
	# チェックした商品の情報を .csv に書き込み
	def write_item_csv(self,file_name):
		item_csv = pd.DataFrame([],columns=["商品名", "url", "quantity", "stock_flg"])
		for i,item in enumerate(self.item_list):
			item_csv.loc[str(i)]=[item.name, item.url, item.quantity, item.stock_flg]
		
		item_csv.to_csv(file_name)

	# 登録された商品をチェックしてツイート。tweet_mode : all-全て、 instock-入庫、 shortage-欠品
	def check_stock( self,api, tweet_mode="instock_shortage" ):
		driver = set_driver()
		for i in self.item_list:
			driver.get(i.url)
			driver.implicitly_wait(2)
			# time.sleep(2)
			item_elm = driver.find_elements_by_id("add-to-cart-button")
			# 「カートに入れる」は有るか？
			if len(item_elm)>0:
				stock = True
				i.quantity=1
			else:
				stock = False
				i.quantity=0
			
			# tweet_mode に合致するアイテムを tweet
			if tweet_mode=="instock_shortage":
				if i.quantity>0 and i.stock_flg==False:
					api.update_status(f"{i.name}　の在庫は、有ります。")
				if i.quantity==0 and i.stock_flg==True:
					api.update_status(f"{i.name}　の在庫が、無くなりました。")
			elif tweet_mode=="all":
				# 全部つぶやく
				api.update_status(f"{i.name}、在庫数:{i.quantity}")
			i.stock_flg = stock
		
		driver.quit()
		self.write_item_csv("amazon_item.csv")



def main():
	# 環境変数をsetting.env > settings.py から取得
	API_KEY = settings.API_KEY
	API_SECRET = settings.API_SECRET
	ACCESS_TOKEN = settings.ACCESS_TOKEN
	ACCESS_SECRET = settings.ACCESS_SECRET

	auth=tweepy.OAuthHandler(API_KEY,API_SECRET)
	auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)
	api=tweepy.API(auth)
	

	# アイテムデータ.csv をStock_check() クラスに読み込む
	amazon_item = Stock_Check()
	amazon_item.read_item_csv("amazon_item.csv")
	
	# 登録された商品の在庫をチェック
	amazon_item.check_stock(api)
	

if __name__ == "__main__":
	main()