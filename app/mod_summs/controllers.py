from flask import Blueprint, render_template, redirect, url_for
from app.mod_summs.forms import SummonerForm

import config, requests

mod_summs = Blueprint("summs", __name__, url_prefix="/summoner")

@mod_summs.route("/", methods=["GET", "POST"])
def index():
	form = SummonerForm()

	if form.validate_on_submit():
		args = { "api_key": config.API["api_key"] }

		summoner_request = "https://la1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}".format(form.summoner_name.data)
		summoner_response = requests.get(summoner_request, args)
		summoner_json = summoner_response.json()

		profile_icon_url = "http://ddragon.leagueoflegends.com/cdn/7.10.1/img/profileicon/{}.png".format(summoner_json["profileIconId"])


		positions_request = "https://la1.api.riotgames.com/lol/league/v3/positions/by-summoner/{}".format(summoner_json["id"])
		positions_response = requests.get(positions_request, args)
		positions_json = positions_response.json()
		soloq = {}
		flex = {}

		validate_positions = len(positions_json)

		if validate_positions > 1:
			guessing_position = { "soloq": positions_json[0], "flex": positions_json[1] }
			soloq = guessing_position["soloq"]
			flex = guessing_position["flex"]
		elif validate_positions > 0:
			guessing_position = { "rank": positions_json[0]}
			rank = guessing_position["rank"]
			if rank["queueType"] == "RANKED_FLEX_SR":
				flex = guessing_position["rank"]
				soloq = { "tier": "UNRANKED" }
			else:
				soloq = guessing_position["rank"]
				flex = { "tier": "UNRANKED" }
		else:
			soloq = { "tier": "UNRANKED" }
			flex = { "tier": "UNRANKED" }


		matches_request = "https://la1.api.riotgames.com/lol/match/v3/matchlists/by-account/{}/recent".format(summoner_json["accountId"])
		matches_response = requests.get(matches_request, args)
		matches_json = matches_response.json()

		matches = matches_json["matches"]
		last_match = matches[0]


		champion_request = "https://la1.api.riotgames.com/lol/static-data/v3/champions/{}".format(last_match["champion"])
		champion_response = requests.get(champion_request, args)
		champion_json = champion_response.json()

		champ_icon_url = "http://ddragon.leagueoflegends.com/cdn/7.10.1/img/champion/{}.png".format(champion_json["key"])

		return render_template("summs/summ.html", form=form, summoner=summoner_json, p_icon=profile_icon_url, c_icon=champ_icon_url, \
				last_match=last_match, champion=champion_json, matches=matches, soloq=soloq, flex=flex)
	return render_template("summs/summs.html", form=form)
