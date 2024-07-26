import os
import asyncio
import nest_asyncio
import aiohttp
import ssl
import socket
from flask import Flask, render_template, jsonify, request, send_from_directory
from datetime import datetime
from pyppeteer import launch

nest_asyncio.apply()

app = Flask(__name__)

# Directory for screenshots
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

# List of websites to check
websites_to_check = [
    # Add your list of websites here
    'woodsteps.nl', 'woodssteps.nl', 'westra-rvs.nl', 'werkavontuur.nl',
    'weeruusz.nl', 'vriesiaschilderstotaal.nl', 'vriesiaschilders.nl',
    'vdmeer-mechanisatie.nl', 'ultragraphix.nl', 'tuintegelfriesland.nl',
    'theazwaan.nl', 'terrastegelfriesland.nl', 'techschets.nl', 'synergie-salon.nl',
    'sybonline.nl', 'svprojects.nl', 'sv-projects.nl', 'strandcrosslemmer.nl',
    'stellingwerfgym.nl', 'steenhandelfriesland.nl', 'steenhandelboonstra.nl',
    'srussell.nl', 'srussel.nl', 'sportbedankjes.nl', 'sponsorbedankje.nl',
    'sinnewurket.nl', 'schildersbedrijf-jurjenwielinga.nl', 'salt-zucchero.nl',
    'rpserver.nl', 'robertpeterson.nl', 'rgfysio.nl', 'reinouw.nl', 'realsisters.nl',
    'puurrinske.nl', 'promotieteamkoudum.nl', 'projectbureaulink.nl', 'printspiratie.nl',
    'printgroen.nl', 'praktijkdezwaluw.nl', 'postmamotorentechniek.nl', 'postmagroep.nl',
    'postmaautosport.nl', 'petersonwebservices.nl', 'petersontechniek.nl',
    'petersonict.nl', 'permateeknederland.nl', 'permateekfriesland.nl', 'orangevibe.nl',
    'oeverzwaluwen.nl', 'nimdedei.nl', 'mirnserheide.nl', 'manitapostma.nl', 'madeontwerp.nl',
    'little-britain.nl', 'lhommesneek.nl', 'lemonnsalttemplates.nl', 'lemonnsaltconcepts.nl',
    'lemonnsalt.nl', 'lafemmesneek.nl', 'labelskopen.nl', 'kunststofteakfriesland.nl',
    'kunststofteakdekken.nl', 'krect.nl', 'koudumerskutsje.nl', 'kofjehuske.nl',
    'kiemmethode.nl', 'kickerkindermode.nl', 'kickerha-ra.nl', 'kerklekkum.nl',
    'jacobvisserschilderwerken.nl', 'ideetechniek.nl', 'iambornfree.nl',
    'huismanwoonbemiddeling.nl', 'huismanvastgoedbemiddeling.nl', 'huisman-makelaars.nl',
    'hmenginesparts.nl', 'glasserviceterpstra.nl', 'ggswinkel.nl', 'ggsgaastgrafischspecialist.nl',
    'gcwergea.nl', 'frisiainvest.nl', 'frieslandsteenhandel.nl', 'friesepalingroker.nl',
    'flexiteekfriesland.nl', 'filmke.nl', 'facility-hospitality.nl', 'facebodycareunique.nl',
    'eetcafespoorzicht.nl', 'destedspolle.nl', 'delaserkliniek.nl', 'degraafwatersport.nl',
    'defriesemerentandarts.nl', 'danilareizen.nl', 'cooperatiegeboortekracht.nl',
    'classiccardealer.nl', 'campingzonneheuvel.nl', 'bouwservicevanderwal.nl',
    'bouwservicedvdwal.nl', 'bouwemeidouwe.nl', 'bouwbedrijfvdwal.nl',
    'bouwbedrijfvdbeek.nl', 'bouwbedrijfvandebeek.nl', 'boostvoorondernemers.nl',
    'boonstrasteenhandel.nl', 'billysfarm.nl', 'beautysalondezwaluw.nl', 'basoosterbaan.nl',
    'bandstrafinancieeladvies.nl', 'avandergootwaterwerken.nl', 'autorijschooltheazwaan.nl',
    'automotorenrevisie.nl', 'automotorenonderdelen.nl', 'ateliernimdedei.nl',
    'alfaserviceassen.nl', 'alfamotiveassen.nl', 'activiteitencentrumplak.nl'
]

import requests

def check_site_health(url):
    try:
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 200:
            return {"url": url, "status": "up", "status_code": response.status_code}
        else:
            return {"url": url, "status": "down", "status_code": response.status_code}
    except Exception as e:
        return {"url": url, "status": "error", "error": str(e)}

@app.route('/')
def index():
    results = {}
    for website in websites_to_check:
        result = check_site_health(f"http://{website}")
        results[website] = result
    return render_template('index.html', all_results=results)

@app.route('/refresh_all', methods=['POST'])
async def refresh_all():
    tasks = [capture_screenshot(f"http://{website}", f"screenshots/{website}.png") for website in websites_to_check]
    await asyncio.gather(*tasks)
    return jsonify({"status": "refreshed"})

@app.route('/add_website', methods=['POST'])
async def add_website():
    data = await request.get_json()
    website = data['url']
    if website not in websites_to_check:
        websites_to_check.append(website)
        await capture_screenshot(f"http://{website}", f"screenshots/{website}.png")
    return jsonify({"status": "added", "url": website})

@app.route('/rescreenshot', methods=['POST'])
async def rescreenshot():
    data = await request.get_json()
    url = data['url']
    domain = url.split("//")[-1]
    await capture_screenshot(url, f"screenshots/{domain}.png")
    return jsonify({"status": "rescreenshot", "url": url})

@app.route('/screenshots/<path:filename>')
def screenshots(filename):
    return send_from_directory('screenshots', filename)

async def capture_screenshot(url, filename):
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle2'})
    await page.screenshot({'path': filename, 'fullPage': True})
    await browser.close()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)