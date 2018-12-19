from bottle import route
from bottle import static_file
import bottle
import json
import MyScholar
@route('/')
def page_index():
    return static_file('/Web/index.html' , root="")

@route('/People')
def page_author():
    name= bottle.request.query.name
    return static_file('/Web/Author.html' , root="")


@route('/js/<filepath:path>')
def server_js(filepath):
    return static_file(filepath, root='Web/js')

@route('/css/<filepath:path>')
def server_css(filepath):
    return static_file(filepath, root='Web/css')
@route('/fonts/<filepath:path>')
def server_fonts(filepath):
    return static_file(filepath, root='Web/fonts')

@route('/images/<filepath:path>')
def server_img(filepath):
    return static_file(filepath, root='Web/images')

@bottle.post('/peoples')
def get_peoples():
    with open("Data/People.json",'r')as f:
         return f.read()

@bottle.post('/getinfo')
def get_people():
    content = bottle.request.body.read().decode()
    with open("Data/"+content.replace('%20','')+".json",'r')as f:
        return f.read()

@bottle.post('/send')
def addpeople():
    content = bottle.request.body.read().decode()
    content = json.loads(content)
    MyScholar.Get(content['name'])

bottle.run(host='localhost', port=8080)