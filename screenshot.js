const puppeteer = require('puppeteer');
const fs = require('fs');

async function captureScreenshot(url, filename) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    try {
        await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 }); // Ensuring the URL is properly loaded
        await page.screenshot({ path: filename });
    } catch (error) {
        console.error(`Failed to capture screenshot for ${url}:`, error);
    } finally {
        await browser.close();
    }
}

const websites = [
    'http://woodsteps.nl', 'http://woodssteps.nl', 'http://westra-rvs.nl', 'http://werkavontuur.nl',
    'http://weeruusz.nl', 'http://vriesiaschilderstotaal.nl', 'http://vriesiaschilders.nl',
    'http://vdmeer-mechanisatie.nl', 'http://ultragraphix.nl', 'http://tuintegelfriesland.nl',
    'http://theazwaan.nl', 'http://terrastegelfriesland.nl', 'http://techschets.nl', 'http://synergie-salon.nl',
    'http://sybonline.nl', 'http://svprojects.nl', 'http://sv-projects.nl', 'http://strandcrosslemmer.nl',
    'http://stellingwerfgym.nl', 'http://steenhandelfriesland.nl', 'http://steenhandelboonstra.nl',
    'http://srussell.nl', 'http://srussel.nl', 'http://sportbedankjes.nl', 'http://sponsorbedankje.nl',
    'http://sinnewurket.nl', 'http://schildersbedrijf-jurjenwielinga.nl', 'http://salt-zucchero.nl',
    'http://rpserver.nl', 'http://robertpeterson.nl', 'http://rgfysio.nl', 'http://reinouw.nl', 'http://realsisters.nl',
    'http://puurrinske.nl', 'http://promotieteamkoudum.nl', 'http://projectbureaulink.nl', 'http://printspiratie.nl',
    'http://printgroen.nl', 'http://praktijkdezwaluw.nl', 'http://postmamotorentechniek.nl', 'http://postmagroep.nl',
    'http://postmaautosport.nl', 'http://petersonwebservices.nl', 'http://petersontechniek.nl',
    'http://petersonict.nl', 'http://permateeknederland.nl', 'http://permateekfriesland.nl', 'http://orangevibe.nl',
    'http://oeverzwaluwen.nl', 'http://nimdedei.nl', 'http://mirnserheide.nl', 'http://manitapostma.nl', 'http://madeontwerp.nl',
    'http://little-britain.nl', 'http://lhommesneek.nl', 'http://lemonnsalttemplates.nl', 'http://lemonnsaltconcepts.nl',
    'http://lemonnsalt.nl', 'http://lafemmesneek.nl', 'http://labelskopen.nl', 'http://kunststofteakfriesland.nl',
    'http://kunststofteakdekken.nl', 'http://krect.nl', 'http://koudumerskutsje.nl', 'http://kofjehuske.nl',
    'http://kiemmethode.nl', 'http://kickerkindermode.nl', 'http://kickerha-ra.nl', 'http://kerklekkum.nl',
    'http://jacobvisserschilderwerken.nl', 'http://ideetechniek.nl', 'http://iambornfree.nl',
    'http://huismanwoonbemiddeling.nl', 'http://huismanvastgoedbemiddeling.nl', 'http://huisman-makelaars.nl',
    'http://hmenginesparts.nl', 'http://glasserviceterpstra.nl', 'http://ggswinkel.nl', 'http://ggsgaastgrafischspecialist.nl',
    'http://gcwergea.nl', 'http://frisiainvest.nl', 'http://frieslandsteenhandel.nl', 'http://friesepalingroker.nl',
    'http://flexiteekfriesland.nl', 'http://filmke.nl', 'http://facility-hospitality.nl', 'http://facebodycareunique.nl',
    'http://eetcafespoorzicht.nl', 'http://destedspolle.nl', 'http://delaserkliniek.nl', 'http://degraafwatersport.nl',
    'http://defriesemerentandarts.nl', 'http://danilareizen.nl', 'http://cooperatiegeboortekracht.nl',
    'http://classiccardealer.nl', 'http://campingzonneheuvel.nl', 'http://bouwservicevanderwal.nl',
    'http://bouwservicedvdwal.nl', 'http://bouwemeidouwe.nl', 'http://bouwbedrijfvdwal.nl',
    'http://bouwbedrijfvdbeek.nl', 'http://bouwbedrijfvandebeek.nl', 'http://boostvoorondernemers.nl',
    'http://boonstrasteenhandel.nl', 'http://billysfarm.nl', 'http://beautysalondezwaluw.nl', 'http://basoosterbaan.nl',
    'http://bandstrafinancieeladvies.nl', 'http://avandergootwaterwerken.nl', 'http://autorijschooltheazwaan.nl',
    'http://automotorenrevisie.nl', 'http://automotorenonderdelen.nl', 'http://ateliernimdedei.nl',
    'http://alfaserviceassen.nl', 'http://alfamotiveassen.nl', 'http://activiteitencentrumplak.nl'
];

(async () => {
    if (!fs.existsSync('screenshots')) {
        fs.mkdirSync('screenshots');
    }
    for (let website of websites) {
        const domain = website.replace('http://', '').replace('https://', '').replace('/', '');
        await captureScreenshot(website, `screenshots/${domain}.png`);
    }
})();