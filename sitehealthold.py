import aiohttp
import asyncio
import nest_asyncio
from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import subprocess

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

app = Flask(__name__)

@app.route('/screenshots/<path:filename>')
def screenshots(filename):
    if not os.path.exists(os.path.join('screenshots', filename)):
        domain = filename.replace('.png', '')
        url = f'http://{domain}'
        capture_screenshot(url, os.path.join('screenshots', filename))
    return send_from_directory('screenshots', filename)

async def check_website(session, website):
    result = {
        'status': 'error',
        'status_code': None,
        'error': None,
        'details': None
    }

    try:
        async with session.get(f"http://{website}", timeout=10, allow_redirects=True) as response:
            result['status_code'] = response.status
            if 200 <= response.status < 400:  # Consider any 2xx and 3xx status as "up"
                result['status'] = 'up'
            else:
                result['status'] = 'down'
            result['details'] = {
                'headers': dict(response.headers),
                'redirects': [str(r.url) for r in response.history],
                'final_url': str(response.url),
                'content_type': response.content_type
            }
    except Exception as e:
        result['error'] = str(e)

    if result['status'] == 'error' or result['status'] == 'down':
        try:
            async with session.get(f"https://{website}", timeout=10, allow_redirects=True) as response:
                result['status_code'] = response.status
                if 200 <= response.status < 400:  # Consider any 2xx and 3xx status as "up"
                    result['status'] = 'up'
                else:
                    result['status'] = 'down'
                result['details'] = {
                    'headers': dict(response.headers),
                    'redirects': [str(r.url) for r in response.history],
                    'final_url': str(response.url),
                    'content_type': response.content_type
                }
        except Exception as e:
            result['error'] = str(e)

    return result

async def check_website_status(websites):
    status = {}

    async with aiohttp.ClientSession() as session:
        tasks = []
        for website in websites:
            tasks.append(check_website(session, website))

        results = await asyncio.gather(*tasks)
        status = {website: result for website, result in zip(websites, results)}

    return status

@app.route('/')
def index():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    all_results = loop.run_until_complete(check_website_status(websites_to_check))
    return render_template('index.html', all_results=all_results)

@app.route('/rescreenshot', methods=['POST'])
async def rescreenshot():
    data = request.json
    url = data['url']
    domain = url.replace('http://', '').replace('https://', '').replace('/', '')
    filename = f'screenshots/{domain}.png'
    
    capture_screenshot(url, filename)

    async with aiohttp.ClientSession() as session:
        result = await check_website(session, domain)
    
    return jsonify({
        'status': 'success',
        'filename': filename,
        'result': result
    })

@app.route('/refresh_all', methods=['POST'])
async def refresh_all():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for website in websites_to_check:
            tasks.append(check_website(session, website))

        results = await asyncio.gather(*tasks)
        status = {website: result for website, result in zip(websites_to_check, results)}

        for website in websites_to_check:
            filename = f'screenshots/{website}.png'
            capture_screenshot(f"http://{website}", filename)

    return jsonify(status)

@app.route('/add_website', methods=['POST'])
async def add_website():
    data = request.json
    url = data['url']
    domain = url.replace('http://', '').replace('https://', '').replace('/', '')
    if domain not in websites_to_check:
        websites_to_check.append(domain)
    filename = f'screenshots/{domain}.png'

    capture_screenshot(url, filename)

    async with aiohttp.ClientSession() as session:
        result = await check_website(session, domain)

    return jsonify({
        'status': 'success',
        'filename': filename,
        'result': result
    })

def capture_screenshot(url, filename):
    subprocess.run(['python', 'capture_screenshot.py', url, filename])

# List of websites to check
websites_to_check = [
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
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)