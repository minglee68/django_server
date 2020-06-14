from selenium import webdriver
from bs4 import BeautifulSoup

def crawl_players():
	from string import ascii_lowercase
	import re

	ORIG_URL = "https://www.basketball-reference.com/"

	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)

	player_list = []
	error_list = []
	for idx in ascii_lowercase:
		if idx == 'x':
			continue

		url = ORIG_URL + "players/" + idx
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

if __name__ == "__main__":
	crawl_players()
