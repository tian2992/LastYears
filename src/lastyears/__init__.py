# -*- coding: utf-8 -*-
import os
import sys
import datetime

if 'site-packages' not in sys.path:
  sys.path.append(os.path.join(os.path.dirname(__file__), "site-packages"))

from flask import Flask
from flask import request
from flask import render_template

app = Flask('lastyears')

import keys

from pyechonest import config
config.ECHO_NEST_API_KEY=keys.ECHONEST_API_KEY

import pylast
lastfm = pylast.LastFMNetwork(api_key=keys.LASTFM_API_KEY, api_secret=keys.LASTFM_SECRET)


def get_lastfm_user(username_string):
  #TODO: verify username_string is clean from nasty stuff
  user = lastfm.get_user(username_string)
  try:
    app.logger.info("User: {0}, id: {1}".format(user.get_name(),user.get_id()))
    return user
  except pylast.WSError:
    app.logger.error("User {0} is not valid".format(user.get_name()))
    return None

def album_info(album):
  """
    converts an album object into a dict with the artist name, the album_name,
      the release date and the album object.
    it is conservative, as some of the requests do hit the network
      and have no cache so it's better to avoid waste
  """
  #TODO: Try cacheing this stuff

  artist = album.get_artist()
  album_name = album.get_name()
  try:
    release_date = datetime.datetime.\
    strptime(album.get_release_date(),"%d %b %Y, %H:%M")
  except:
    release_date = None # = datetime.datetime(1900,1,1)
  raw_album = album
  return {'artist':artist, 'album_name':album_name,
          'release_date':release_date, 'raw_album':raw_album}

def date_year_average(list):
  date_list = [x for x in list if x != None]
  return reduce(lambda x,y: x+y, map(lambda da: da.year, date_list))/len(date_list)



@app.route('/')
def hello():
  return render_template("index.html")

@app.route('/albums',methods=['GET'])
def get_user_page():
  username_string = request.args.get("username",'')
  lastfm_user = get_lastfm_user(username_string)


  if (not lastfm_user):
    #TODO: add fancy fail screen
    return ("Don't be boring, have a username",404)

  #li = map(lambda x : str(x[0]), top_albums_list)
  #li = map(lambda x : (str(x[0]),x[0].get_release_date()), top_albums_list)
  #date_o = datetime.datetime.strptime(date_s,"%d %b %Y, %H:%M")

  top_albums_list = map(lambda x: album_info(x[0]), lastfm_user.get_top_albums())
  date_average = date_year_average(map(lambda x: x["release_date"],top_albums_list))

  return render_template("album_list.html", user = lastfm_user,
    album_list = top_albums_list, average = date_average)

