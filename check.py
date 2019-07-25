from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
import urllib.request
from bs4 import BeautifulSoup
import json
import re

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Fetch GitTop',
    description='A simple API to fetch github top stars repo',
)

ns = api.namespace('github', description='Github Top Starred Repo Extracter')

todo = api.model('githhub', {
    'organization': fields.String(required=True, description='The task details')
})

res = api.model('results', {
    'name': fields.String(required=True, description='The task details'),
    'stars': fields.String(required=True, description='The task details')
})



@ns.route('/')
class TodoList(Resource):
    '''Get top repo of a organization'''
    @ns.doc('github')
    @ns.expect(todo)
    @ns.marshal_with(res, code=201)
    def post(self):
        '''Create a new task'''
        orgname = api.payload
        orgname = orgname['organization']
        url = "https://github.com/search?o=desc&q=" + orgname +"&s=stars&type=Repositories"
        request = urllib.request.Request(url)
        html = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(html,'html.parser')
        container = soup.findAll("li", {"class":"repo-list-item d-flex flex-column flex-md-row flex-justify-start py-4 public source"})
        git_dict = []
        for i in range(0, 3):
            g_dict = {}
            t = container[i].findAll("a",{"class":"v-align-middle"})
            y = container[i].findAll("a",{"class":"muted-link"})
            p = re.findall(r'\d.+',str(y))
            t = str(t)
            r = t.split(sep=">")
            x = str(r[-2])
            list_final = x.split(sep='<')
            g_dict['name'] = list_final[0]
            g_dict['stars'] = p[-1]
            git_dict.append(g_dict)
        
        return git_dict,201



if __name__ == '__main__':
    app.run(debug=True)