from flask import Flask, render_template
import requests
import sys

app = Flask(__name__)


@app.route('/')
def mainPage():
    # this is the main route which opens the forms for three other routes
    return render_template('index.html', **locals())


@app.route('/listSpecies')
@app.route('/listSpecies/limit=<int:limit>')
def listSpecies(limit=None):
    # this route list all the species either with a limit or all of them

    # this is the main server
    server = "http://rest.ensembl.org"
    # this is the route to get all the species
    ext = "/info/species?"

    # this function performs the request to get all data in the form of json
    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

    # if request is not completes an error is thrown
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    # the json data is then decoded and stored as a dict
    decoded = r.json()
    # this condition checks whether to apply a limit or list all of the species
    if (limit == None):
        temp = decoded['species'][:]
    else:
        temp = decoded['species'][:limit]
    # the data is then sent to html file to render
    return render_template('listSpecies.html', **locals())


@app.route('/karyotype/specie=<string:specie>')
def karyotypeInfo(specie):
    # this route shows the info for the karyotype of the specie

    # main server
    server = "http://rest.ensembl.org"
    # route to get the specie data
    ext = "/info/assembly/" + specie + "?"

    # request to get data in json format
    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

    # connection error condition
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    # decoded json string
    decoded = r.json()
    temp = decoded['karyotype']
    # data is sent to html to render info
    return render_template('karyotype.html', **locals())


@app.route('/chromosomeLength/specie=<string:specie>/chromo=<string:chromo>')
def getChromo(specie, chromo):
    # this route renders the info about given species chromosome
    server = "http://rest.ensembl.org"
    ext = "/info/assembly/" + specie + "?"

    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()
    decoded = r.json()
    temp = decoded['top_level_region']
    # this condidion matches the given chromosome name and saves its info in temp
    for i in temp:
        if (i['name'] == chromo):
            temp = i
    # after which the data is rendered
    return render_template('chromosomeLength.html', **locals())


if __name__ == "__main__":
    # the port number
    # debug mode allow to continiously run the server
    app.run(port=8000, debug=True)