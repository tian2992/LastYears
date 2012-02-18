import datetime
import pylast

from google.appengine.ext import db

class Album(db.Model):
  artist_name = db.StringProperty(required=True)
  album_name = db.StringProperty(required=True)
  release_date = db.DateProperty()

  def __getitem__(self,key):
    if key == "artist":
      return pylast.Artist(self.artist_name,pylast.LastFMNetwork())
    if key == "raw_album":
      return pylast.Album(self.artist_name, self.album_name, pylast.LastFMNetwork())
    if key == "release_date":
      return self.release_date
    raise AttributeError()

