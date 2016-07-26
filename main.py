#!/usr/bin/env python
import os
import jinja2
import webapp2
import json
from google.appengine.api import users
from google.appengine.api import urlfetch
from models import Message

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


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


class MessageHandler(BaseHandler):
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

        return self.render_template("message.html", params)

    def post(self):
        user = users.get_current_user()
        input_message = self.request.get("message")
        #input_sender = self.request.get("sender")
        # second way, direct way to input user to db without input
        input_sender = user.email()
        input_receiver = self.request.get("receiver")

        message = Message(message=input_message, sender=input_sender, receiver=input_receiver)
        message.put()

        return self.write("You have written: " + input_message + " " + input_sender + " " + input_receiver)


class GetAllMessagesHandler(BaseHandler):
    def get(self):
        messages = Message.query().fetch()
        params = {"messages": messages}

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

        return self.render_template("all_messages.html", params=params)


class SingleMessageHandler(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))
        params = {"message": message}

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

        return self.render_template("single_message.html", params=params)


class EditMessageHandler(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))
        params = {"message": message}

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

        return self.render_template("edit_message.html", params=params)

    def post(self, message_id):
        user = users.get_current_user()
        input_message = self.request.get("edit_message")
        #input_sender = self.request.get("edit_sender")
        input_sender = user.email()
        input_receiver = self.request.get("edit_receiver")
        message = Message.get_by_id(int(message_id))

        message.message = input_message
        message.sender = input_sender
        message.receiver = input_receiver
        message.put()
        return self.redirect_to("all-messages")


class DeleteMessageHandler(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))
        params = {"message": message}

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

        return self.render_template("delete_message.html", params=params)

    def post(self, message_id):
        message = Message.get_by_id(int(message_id))
        message.key.delete()
        return self.redirect_to("all-messages")


class SentMessageHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        m_sender = Message.query(Message.sender==user.email()).fetch()
        params = {"m_sender": m_sender}

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

        return self.render_template("sent_mail.html", params=params)


class ReceivedMessageHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        m_receiver = Message.query(Message.receiver==user.email()).fetch()
        params = {"m_receiver": m_receiver}

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

        return self.render_template("received_mail.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/vreme', WeatherHandler),
    webapp2.Route('/message', MessageHandler),
    webapp2.Route('/result', MessageHandler),
    webapp2.Route('/all_messages', GetAllMessagesHandler, name="all-messages"),
    webapp2.Route('/single_message/<message_id:\\d+>', SingleMessageHandler),
    webapp2.Route('/single_message/<message_id:\\d+>/edit', EditMessageHandler),
    webapp2.Route('/single_message/<message_id:\\d+>/delete', DeleteMessageHandler),
    webapp2.Route('/sent_mail', SentMessageHandler),
    webapp2.Route('/received_mail', ReceivedMessageHandler),
], debug=True)
'''
data = open("people.json", "r").read()
json_data = json.loads(data)
params["seznam"] = [json_data]
'''