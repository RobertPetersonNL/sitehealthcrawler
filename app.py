import os
import logging
from flask import Flask, render_template, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.common.exceptions import WebDriverException

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, filename='website_health.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# List of websites to check
websites = [
    "woodsteps.nl", "woodssteps.nl", "westra-rvs.nl", "werkavontuur.nl", "weeruusz.nl",
    "vriesiaschilderstotaal.nl", "vriesiaschilders.nl", "vdmeer-mechanisatie.nl",
    "ultragraphix.nl", "tuintegelfriesland.nl", "theazwaan.nl", "terrastegelfriesland.nl",
    "techschets.nl", "synergie-salon.nl", "sybonline.nl", "svprojects.nl", "sv-projects.nl",
    "strandcrosslemmer.nl", "stellingwerfgym.nl", "steenhandelfriesland.nl", "steenhandelboonstra.nl",
    "srussell.nl", "sportbedankjes.nl", "sponsorbedankje.nl", "sinnewurket.nl", "schildersbedrijf-jurjenwielinga.nl",
    "salt-zucchero.nl", "rpserver.nl", "robertpeterson.nl", "rgfysio.nl", "reinouw.nl", "realsisters.nl",
    "puurrinske.nl", "promotieteamkoudum.nl", "projectbureaulink.nl", "printspiratie.nl", "printgroen.nl",
    "praktijkdezwaluw.nl", "postmamotorentechniek.nl", "postmagroep.nl", "postmaautosport.nl",
    "petersonwebservices.nl", "petersontechniek.nl", "petersonict.nl", "permateeknederland.nl",
    "permateekfriesland.nl", "orangevibe.nl", "oeverzwaluwen.nl", "nimdedei.nl", "mirnserheide.nl",
    "manitapostma.nl", "madeontwerp.nl", "little-britain.nl", "lhommesneek.nl", "lemonnsalttemplates.nl",
    "lemonnsaltconcepts.nl", "lemonnsalt.nl", "lafemmesneek.nl", "labelskopen.nl", "kunststofteakfriesland.nl",
    "kunststofteakdekken.nl", "krect.nl", "koudumerskutsje.nl", "kofjehuske.nl", "kiemmethode.nl", "kickerkindermode.nl",
    "kickerha-ra.nl", "kerklekkum.nl", "jacobvisserschilderwerken.nl", "ideetechniek.nl", "iambornfree.nl",
    "huismanwoonbemiddeling.nl", "huismanvastgoedbemiddeling.nl", "huisman-makelaars.nl", "hmenginesparts.nl",
    "glasserviceterpstra.nl", "ggswinkel.nl", "ggsgaastgrafischspecialist.nl", "gcwergea.nl", "frisiainvest.nl",
    "frieslandsteenhandel.nl", "friesepalingroker.nl", "flexiteekfriesland.nl", "filmke.nl", "facility-hospitality.nl",
    "facebodycareunique.nl", "eetcafespoorzicht.nl", "destedspolle.nl", "delaserkliniek.nl", "degraafwatersport.nl",
    "defriesemerentandarts.nl", "danilareizen.nl", "cooperatiegeboortekracht.nl", "classiccardealer.nl",
    "campingzonneheuvel.nl", "bouwservicevanderwal.nl", "bouwservicedvdwal.nl", "bouwemeidouwe.nl", "bouwbedrijfvdwal.nl",
    "bouwbedrijfvdbeek.nl", "bouwbedrijfvandebeek.nl", "boostvoorondernemers.nl", "boonstrasteenhandel.nl", "billysfarm.nl",
    "beautysalondezwaluw.nl", "basoosterbaan.nl", "bandstrafinancieeladvies.nl", "avandergootwaterwerken.nl",
    "autorijschooltheazwaan.nl", "automotorenrevisie.nl", "automotorenonderdelen.nl", "ateliernimdedei.nl",
    "alfaserviceassen.nl", "alfamotiveassen.nl", "activiteitencentrumplak.nl"
]

website_status = {}


def take_screenshot(url, domain):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    screenshot_path = f'static/screenshots/{domain}.png'
    
    try:
        driver.get(f"http://{domain}")
        driver.set_window_size(1920, 1080)
        driver.save_screenshot(screenshot_path)
        driver.quit()
        return screenshot_path
    except Exception as e:
        driver.quit()
        logging.error(f"Error taking screenshot for {domain}: {e}")
        return None


def check_website(url, domain):
    result = {
        'dns': False,
        'ssl': False,
        'online': False,
        'error': None,
        'screenshot': None,
        'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(f"http://{domain}")
        
        result['online'] = True
        result['screenshot'] = take_screenshot(url, domain)
    except WebDriverException as e:
        result['error'] = str(e)
        logging.error(f"Error checking {domain}: {e}")
    finally:
        driver.quit()
    
    return result


@app.route('/')
def index():
    for website in websites:
        website_status[website] = check_website(website, website)
    return render_template('index.html', results=website_status)


@app.route('/add', methods=['POST'])
def add_website():
    url = request.form['url']
    logging.info(f"Received URL to add: {url}")
    if url and url not in websites:
        websites.append(url)
        website_status[url] = check_website(url, url)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)