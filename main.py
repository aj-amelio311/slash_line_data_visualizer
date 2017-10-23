from flask import Flask, request, render_template, jsonify
import bs4
import pandas
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template("index.html")

@app.route('/process', methods=["POST"])
def process():
	name = request.form['name']
	if name:
		player_age = []
		player_avg = []
		player_slg = []
		player_obp = []
		name_data = name.split();
		fn = name_data[0][:2]
		fl = name_data[1][:1]
		ln = name_data[1][:5]
		url = "https://www.baseball-reference.com/players/" + fl + "/" + ln + fn + "01.shtml"
		url2 = "https://www.baseball-reference.com/players/" + fl + "/" + ln + fn + "02.shtml"
		dupe_check = requests.get(url2)
		def scrape(url_to_pass):
			html = requests.get(url)
			sitemap = bs4.BeautifulSoup(html.text, "lxml")
			overall = sitemap.findAll("tr", {"class": "full"})
			for tags in overall:
				age = tags.findAll("td", {"data-stat": "age"})
				slg = tags.findAll("td", {"data-stat": "slugging_perc"})
				avg = tags.findAll("td", {"data-stat": "batting_avg"})
				obp = tags.findAll("td", {"data-stat": "onbase_perc"})
				for i in age:
					player_age.append(i.text)
				for i in slg:
					player_slg.append(i.text)
				for i in avg:
					player_avg.append(i.text)
				for i in obp:
					player_obp.append(i.text)
			stats = list(zip(player_age, player_avg, player_obp, player_slg))
			global df
			df = pandas.DataFrame(stats, columns=["age", "avg", "obp", "slg"])
			if df.empty:
				return jsonify({
					"empty": "true"
				})
	if dupe_check.status_code != 200:
		scrape(url)
		if url.status_code != 200:
			return jsonify({
				'server': 'false'
			})
		da = df.reindex(columns=["avg"]).to_json()
		do = df.reindex(columns=["obp"]).to_json()
		ds = df.reindex(columns=["slg"]).to_json()
		age_data = df.reindex(columns=["age"]).to_json()
		if not df.empty:
			return jsonify({
				'name': name,
				'avg': da,
				'obp': do,
				'slg': ds,
				'age': age_data,
				'doops': 'false'
			})
	else:
		search_names = []
		search_links = []
		search_url = "https://www.baseball-reference.com/search/search.fcgi?&search=" + name_data[0] + "+" + name_data[1]
		player_dupes_raw = requests.get(search_url)
		dupe_sitemap = bs4.BeautifulSoup(player_dupes_raw.text, "lxml")
		dupes_overall = dupe_sitemap.findAll("div", {"class": "search-item-name"})
		links_overall = dupe_sitemap.findAll('div', {'class': 'search-item-url'})
		for i in dupes_overall:
			search_names.append(i.text)
		for a in links_overall:
			search_links.append(a.text)
		search_data = dict(zip(search_names, search_links))
		searched_name = search_names[0]
		search_link = "https://www.baseball-reference.com" + search_links[0]
		html_search = requests.get(search_link)
		sitemap_search = bs4.BeautifulSoup(html_search.text, "lxml")
		overall_search = sitemap_search.findAll("tr", {"class": "full"})
		search_age = []
		search_avg = []
		search_slg = []
		search_obp = []
		for tags in overall_search:
			age_find = tags.findAll("td", {"data-stat": "age"})
			slg_find = tags.findAll("td", {"data-stat": "slugging_perc"})
			avg_find = tags.findAll("td", {"data-stat": "batting_avg"})
			obp_find = tags.findAll("td", {"data-stat": "onbase_perc"})
			for i in age_find:
				search_age.append(i.text)
			for i in slg_find:
				search_slg.append(i.text)
			for i in avg_find:
				search_avg.append(i.text)
			for i in obp_find:
				search_obp.append(i.text)
		stats_search = list(zip(search_age, search_avg, search_obp, search_slg))
		df_search = pandas.DataFrame(stats_search, columns=["age", "avg", "obp", "slg"])
		da_search = df_search.reindex(columns=["avg"]).to_json()
		do_search = df_search.reindex(columns=["obp"]).to_json()
		ds_search = df_search.reindex(columns=["slg"]).to_json()
		age_search = df_search.reindex(columns=["age"]).to_json()
		return jsonify({
			'search_name': search_names[0],
			'doops': 'true',
			'avg_s': da_search,
			'obp_s': do_search,
			'slg_s': ds_search,
			'age_s': age_search
		})
	return jsonify({'error': 'no data'})

if __name__ == "__main__":
    app.run()
