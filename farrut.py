import click
import os.path
import model
import json
import requests
from tinydb import TinyDB, Query 

req_src = 'db/requests.json'
res_src = 'db/results.json'
log_src = 'db/log.json'

db_req = None
db_res = None
db_log = None

def init_dbs():
    global db_req, db_res,db_log
    db_req = TinyDB(req_src)
    db_res = TinyDB(res_src)
    db_log = TinyDB(log_src)

def validate_and_save_solution(response_json):
    #parse response to dictionary
    response = json.loads(response_json)

    #if error, print it
    if("error" in response):
    	click.echo(json.dumps(response, indent = 2))

    #else save
    else:
        db_res.insert(response)
        click.echo("Response saved!")


@click.group()
def cli():
    """Farrut Flights App
    Damit sich d'wilde zottl und s'farrut kaetzle ganz oft seaha kuennan! :D
    """
    init_dbs()
        
@cli.command()
def init():
  
    """Create database files"""
    if os.path.isfile(req_src) == False:
        open(req_src, 'w+').close()
        click.echo('Created ' + req_src)

    if os.path.isfile(res_src) == False:
        open(res_src,'w+').close()
        click.echo('Created ' + res_src)
        
    if os.path.isfile(log_src) == False:
        open(log_src,'w+').close()
        click.echo('Created ' + log_src)


@cli.group()
def request():
    """Edit your flight requests. You can show all, delete or add entries."""

@request.command()
def add():
    """"Add a new request"""
    
    #Ask user for specification
    origin = raw_input("Origin: ")
    destination = raw_input("Destination: ")
    date_to = model.date.from_std(raw_input("Date to [DD.MM.YYYY]: "))
    date_return = model.date.from_std(raw_input("Date return [DD.MM.YYYY]: ")) 
    sale_country = raw_input("Sale country: ")

    #create request
    slice_to = model.slice(origin,destination,date_to)
    slice_return = model.slice(destination,origin,date_return)
    slices = [slice_to,slice_return]

    my_request = model.request(slices,sale_country)
    
    #add to db
    db_req.insert(my_request.to_dict())

    click.echo('Done!')

@request.command()
@click.argument('id')
def delete(id):
    db_req.remove(eids = [int(id)])
    click.echo("Request with Id =" + str(id) + "deleted!")
    
@request.command()
def show():
    entries = db_req.all()
    click.echo('Id | Origin | Destination | Date | Sale Country' )
    click.echo()
    for req_dict in entries:
        req = model.request.from_dict(req_dict)

        for item in req.slices:
            output = "{id} {ori} {dest} {date} {cntry}".format(id = req_dict.eid, ori = item.origin, dest = item.destination, date = item.date, cntry = req.sale_country)
            click.echo(output)

        click.echo()


@cli.command()
@click.option('--once', is_flag = True)
def run(once):
    #Google API key needs to be passed with each request

    api_key = open('APIkey.txt','r').read()

    url = "https://www.googleapis.com/qpxExpress/v1/trips/search"

    request_url = url + "?key=" + api_key

    if(once):
        for req in db_req.all():
            r = requests.post(request_url, json=req)
            
            validate_and_save_solution(r.text)
