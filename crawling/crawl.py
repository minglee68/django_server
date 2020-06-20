from selenium import webdriver
from bs4 import BeautifulSoup

DRIVER_PATH = "D:\Program\chromedriver.exe"    # Set your chronium path
NBA_ORIG_URL = "https://www.basketball-reference.com"
KBL_ORIG_URL = "https://www.kbl.or.kr"
DEBUG = True

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

def crawl_NBA_players():
	from string import ascii_lowercase

	global DRIVER_PATH
	global chrome_options
	ORIG_URL = NBA_ORIG_URL
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
	global DRIVER_PATH
	global chrome_options
	driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)

	ORIG_URL = KBL_ORIG_URL
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

	global DRIVER_PATH
	global chrome_options
	ORIG_URL = NBA_ORIG_URL
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
	global DRIVER_PATH
	global chrome_options
	driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)

	year_list = range(2014, 2019)
	month_list = range(1, 13)
	ORIG_URL = KBL_ORIG_URL

	game_data_list = []
	for year in year_list:
		for month in month_list:
			url = ORIG_URL + "/schedule/today/calendar.asp?CalDate=" + str(year) + "-" + str(month)
			driver.get(url)
			html = driver.page_source
			soup = BeautifulSoup(html, 'html.parser')

			for game_date in soup.select('.txt_g'):
				game = {}

				link = game_date.find('a').attrs['href']
				url = ORIG_URL + "/schedule/today/" + link
				driver.get(url)
				html = driver.page_source
				soup = BeautifulSoup(html, 'html.parser')

				date = link.split('=')[-1]
				home_team = soup.select(".game_result_board .col_left strong.team_name")[0].get_text()
				away_team = soup.select(".game_result_board .col_right strong.team_name")[0].get_text()

				game['date'] = date
				game['away'] = {}
				game['away']['team'] = away_team
				game['home'] = {}
				game['home']['team'] = home_team

				link = soup.select("#subcontents > iframe")[0].attrs['src']
				url = ORIG_URL + "/schedule/today" + link[1:]
				driver.get(url)
				html = driver.page_source
				soup = BeautifulSoup(html, 'html.parser')

				link = soup.select('.tab5 > li > a')[1].attrs['href']
				url = ORIG_URL + "/schedule/today" + link[1:]
				driver.get(url)
				html = driver.page_source
				soup = BeautifulSoup(html, 'html.parser')

				is_home = True
				for table in soup.select('table.tbltype_p_record'):
					players = []
					for row in table.select("tbody > tr"):
						player = {}
						td_list = row.select('td')
						if len(td_list) < 24:
							continue

						player['name'] = td_list[2].get_text()
						player['mp'] = td_list[3].get_text()
						player['fg'] = td_list[8].get_text().split('/')[0]
						player['fga'] = td_list[8].get_text().split('/')[1]
						player['fg_pct'] = "." + td_list[9].get_text()
						player['fg3'] = td_list[6].get_text().split('/')[0]
						player['fg3a'] = td_list[6].get_text().split('/')[1]
						player['fg3_pct'] = "." + td_list[7].get_text()
						player['ft'] = td_list[10].get_text().split('/')[0]
						player['fta'] = td_list[10].get_text().split('/')[1]
						player['ft_pct'] = "." + td_list[11].get_text()
						player['orb'] = td_list[12].get_text()
						player['drb'] = td_list[13].get_text()
						player['trb'] = td_list[14].get_text()
						player['ast'] = td_list[16].get_text()
						player['stl'] = td_list[18].get_text()
						player['blk'] = td_list[19].get_text()
						player['tov'] = td_list[17].get_text()
						player['pf'] = td_list[20].get_text()
						player['pts'] = td_list[23].get_text()

						players.append(player)
						print(player)

					if is_home:
						game['home']['players'] = players
						is_home = not is_home
					else:
						game['away']['players'] = players
						is_home = not is_home
				game_data_list.append(game)
	return game_data_list

if __name__ == "__main__":
	import json
	# data = crawl_KBL_players()
	# data = crawl_KBL_gamePlayerStat()
	# print(json.dumps(data, indent=4))
