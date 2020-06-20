from selenium import webdriver
from bs4 import BeautifulSoup

DRIVER_PATH = "D:\Program\chromedriver.exe"    # Set your chronium path
ORIG_URL = "https://www.basketball-reference.com"
DEBUG = True

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

def crawl_NBA_players():
	from string import ascii_lowercase

	global ORIG_URL
	global DRIVER_PATH
	global chrome_options
	driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)

	player_list = []
	error_list = []
	for idx in ascii_lowercase:
		if idx == 'x':
			continue

		url = ORIG_URL + "/players/" + idx
		driver.get(url)
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')

		# MAYBE isAvtice attribute is needed in player schema
		for link in soup.select("#players tbody th strong a"): # Only for Active players
		# for link in soup.select("#players tbody th a"): # For all players
			link = link.attrs['href']

			driver.get(ORIG_URL + link)
			html = driver.page_source
			soup = BeautifulSoup(html, 'html.parser')

			metadata = {}

			img = soup.select("#meta > div > img")
			if len(img) == 0:
				img = "https://via.placeholder.com/150"
			else:
				img = img[0].attrs['src']
			metadata['img'] = img

			try:
				metadata['name'] = soup.select("#meta > div:nth-last-of-type(1) > h1")[0].get_text()

				metalist = soup.select("#meta > div:nth-last-of-type(1) > p")
				for idx, data in enumerate(metalist):
					data = " ".join(data.get_text().split())
					if (data.startswith("Position:")):
						data = " ".join(data.split()[1:-3])
						metadata['position'] = [x.strip() for x in data.split("and")]
					elif (data[0].isdecimal()):
						metadata['height'] = int(data.split("(")[1].split("c")[0])
						metadata['weight'] = int(data.split(",")[2].split("k")[0].strip())
					elif (data.startswith("Born:")):
						metadata['age'] = int(data.split(":")[2].split("-")[0].strip())
						break
				player_list.append(metadata)
			except Exception as e:
				print(e)
				error_list.append(link)
				continue

			if DEBUG:
				print(metadata['name'], end=' ')
				print(metadata['position'], end=' ')
				print(str(metadata['height']) + " " + str(metadata['weight']) + " " + str(metadata['age']))

	return player_list, error_list

def crawl_KBL_players():
	import datetime

	global ORIG_URL
	global DRIVER_PATH
	global chrome_options
	driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)

	ORIG_URL = "https://www.kbl.or.kr"
	temp_url = ORIG_URL + "/players/player_list.asp"

	player_list = []

	driver.get(temp_url)
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')
	for team in soup.select("div.srch_team li"):
		link_t = team.find('a').attrs['href']

		for flag2 in range(0, 2):
			link = "?flag2=" + str(flag2) + "&" + link_t.split('&')[-1]
			url = temp_url + link

			driver.get(url)
			html = driver.page_source
			soup = BeautifulSoup(html, 'html.parser')

			team_name = soup.select("div.seqlist > dl > dd")[0].get_text()
			for player in soup.select("div.seqlist li"):
				player_data = {}

				link = player.find('a').attrs['href']
				player_data['name'] = player.get_text().strip().split('[')[0]
				player_data['position'] = "".join(player.get_text().split()).split('[')[-1].split(']')[0]

				driver.get(ORIG_URL + link)
				html = driver.page_source
				soup = BeautifulSoup(html, 'html.parser')

				player_data['age'] = datetime.date.today().year - int(soup.select('.birth')[0].get_text().split('.')[0]) + 1
				player_data['height'] = int(float(soup.select('.stature')[0].get_text().split('c')[0]))
				player_data['img'] = ORIG_URL + soup.select("div.frame_g img")[0].attrs['src']
				player_data['team'] = team_name

				player_list.append(player_data)

				if DEBUG:
					print(player_data['name'], end=' ')
					print(player_data['position'], end=' ')
					print(str(player_data['height']) + " " + str(player_data['age']))

	return player_list

def crawl_NBA_gamePlayerStat():
	day_list = ["october", "november", "december", "january", "february", "march", "april", "may", "june"]
	year_list = range(2014, 2019)

	global ORIG_URL
	global DRIVER_PATH
	global chrome_options
	driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)

	game_data_list = []
	for year in year_list:
		for day in day_list:
			url = ORIG_URL + "/leagues/NBA_" + str(year) + "_games-" + day + ".html"
			driver.get(url)
			html = driver.page_source
			soup = BeautifulSoup(html, 'html.parser')

			for link in soup.select("#schedule > tbody > tr > td:nth-of-type(6) > a"):
				if DEBUG:
					print(link)
				game_data = {}
				link = link.attrs['href']
				game_data['date'] = link.split('/')[-1][:8]

				driver.get(ORIG_URL + link)
				html = driver.page_source
				soup = BeautifulSoup(html, 'html.parser')

				is_home = False
				for table in soup.select(".now_sortable"):
					if not table.get('id').endswith("-game-basic"):
						continue

					game = {}
					game["team"] = table.find("caption").get_text().split('(')[0].strip()
					team_list = []
					for row in table.select("tbody tr"):
						if row.attrs.get('class') is not None:
							continue

						player = {}
						player['name'] = row.find('th').get_text()
						for col in row.select("td"):
							player[col.attrs["data-stat"]] = col.get_text()

						team_list.append(player)
					game["players"] = team_list

					if is_home:
						if game_data.get('home'):
							print("error")
						game_data['home'] = game
					else:
						if game_data.get('away'):
							print("error")
						game_data['away'] = game

					is_home = not is_home
				game_data_list.append(game_data)
	return game_data_list

def crawl_KBL_gamePlayerStat():
	pass

if __name__ == "__main__":
	import json
	data = crawl_KBL_players()
	#data = crawl_NBA_gamePlayerStat()
	print(json.dumps(data, indent=4))
