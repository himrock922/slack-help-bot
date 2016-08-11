# - *- coding: utf-8 -*
import time
import re
import signal
import os
import multiprocessing as mp
from slackclient import SlackClient
from token_restore import TokenInput

class SlackHelpBot:
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  # Token Conf read 
  token = ""
  try:
    rfile = open("token.txt", "r")
  except IOError:
    print("token.txt cannot be opened.")
    TokenInput().run()
    wfile = open("token.txt", "w")
    wfile.writelines(token)
    wfile.close
    rfile = open("token.txt", "r")
  else:
    token = rfile.readline()
    rfile.close
  ######################

  sc = SlackClient(token)
  def __init__(self):
    if SlackHelpBot.sc.rtm_connect():
      while True:
        data = SlackHelpBot.sc.rtm_read()

        if len(data) > 0:
          for item in data:
            SlackHelpBot.sc.rtm_send_message("test-help-bot", self.create_message(item))
            time.sleep(1)
    else:
      print("Connection Failed, invalid token?")
 
  def create_message(self, data):
    if "type" in data.keys():
      if data["type"] == "message":
        if re.search(u"(.*帰ります.*|.*帰宅.*)", data["text"]) is not None:
          return "<@" + data["user"] + "> " + u"お疲れ様〜。気をつけて帰ってきてね！:wink:"

sbm = SlackHelpBot()