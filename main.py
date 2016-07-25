#!/usr/bin/env python
import os
import jinja2
import webapp2
import json
from google.appengine.api import users
from google.appengine.api import urlfetch

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            prijavljen = True
            logout_url = users.create_logout_url('/')

            params = {"prijavljen": prijavljen, "logout_url": logout_url, "user": user}
        else:
            prijavljen = False
            login_url = users.create_login_url('/')

            params = {"prijavljen": prijavljen, "login_url": login_url, "user": user}

        return self.render_template("hello.html", params=params)

class WeatherHandler(BaseHandler):
    def get(self):
        url = "http://api.openweathermap.org/data/2.5/weather?q=Ljubljana,svn&appid=555d2db65137ecbbd820613da4006d3d"

        result = urlfetch.fetch(url)

        url_podatki = json.loads(result.content)

        params = {"podatki": url_podatki}

        user = users.get_current_user()

        params["user"] = user

        if user:
            prijavljen = True
            logout_url = users.create_logout_url('/')

            params["prijavljen"] = prijavljen
            params["logout_url"] = logout_url
        else:
            prijavljen = False
            login_url = users.create_login_url('/')

            params["prijavljen"] = prijavljen
            params["login_url"] = login_url

        return self.render_template("vreme.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/vreme', WeatherHandler)
], debug=True)
'''
data = open("people.json", "r").read()
json_data = json.loads(data)
params["seznam"] = [json_data]
'''