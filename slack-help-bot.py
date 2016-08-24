# - *- coding: utf-8 -*
import time
import re
import signal
import os
import sys
import argparse
from slackclient import SlackClient
from token_restore import TokenInput

class SlackHelpBot:
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  def __init__(self):
    token = ""
    status = 0
    heroku_time = 21600
    channel = ""
    # Parse Set
    parser = argparse.ArgumentParser(prog='python slack-help-bot.py')
    parser.add_argument("-t", "--token", type=str, default="", help="Slack Access Token") # Store Token
    parser.add_argument("-c", "--channel", default="", help="Slack Channel") # Store Channel
    args = parser.parse_args()
    #########################
    # Token Conf read
    if args.token:
      token = args.token
      sc = SlackClient(token)
    else:
      token = TokenInput()
      sc = SlackClient(token.info())
    ######################
    # Check read API Token
    api_test = sc.api_call("api.test")
    if api_test["ok"] == status:
      self.error_message(api_test["error"])
    ######################
    # ouput of own bot info
    rtm_start = sc.api_call("rtm.start")
    if rtm_start["ok"] == status:
      self.error_message(rtm_start["error"])
    #######################
    bot_info = rtm_start['self']
    bot_id = bot_info["id"]
    # Channel Info read
    if args.channel:
      channel = args.channel
    else:
      channel = self.restore_channel_list(sc, status)
    print("Join Channel:" + channel)
    if sc.rtm_connect():
      while True:
        data = sc.rtm_read()
        if len(data) > 0:
          for params in data:
             if "type" in params.keys():
               if params["type"] == "message":
                 if re.search(bot_id, params["text"]):
                   if re.search(u"(.*sleep.*)", params["text"]) is not None:
                     self.sleep_message(sc, params, heroku_time, channel)
                   elif re.search(u"(.*mention.*|.*返信.*)", params["text"]) is not None:
                     self.mention_help_message(params, sc, channel)
                   else:
                     self.default_message(params, sc, channel)
    else:
      print("Connection Failed, invalid token?")

  # restore of channel list
  def restore_channel_list(self, sc, status):
    message_channel = ""
    try:
      rfile = open("channel_list.txt", "r")
    except IOError:
      print("channel_list.txt cannnot be opened.")
      print("File create of channel_list.txt.")
      wfile = open("channel_list.txt", "w+")
      channel_list = sc.api_call("channels.list")
      if channel_list["ok"] == status:
        self.error_message(channel_list["error"])
      for channel in channel_list["channels"]:
        if channel["name"].find("test-help-bot") >= 0:
          channel = channel["name"]
        wfile.write(channel["name"])
        wfile.write('\n')
    else:
      channel_list = rfile.readlines()
      for channel in channel_list:
        if channel.find("test-help-bot") >= 0:
          message_channel = channel
    finally:
      return message_channel.strip()

  # Default Message of Bot.
  def default_message(self, params, sc, channel):
    sc.rtm_send_message(channel, "<@" + params["user"] + "> " + u"ごめんw それ分からないw")
  #####################

  # Mention Help Message of Bot.
  def mention_help_message(self, params, sc, channel):
    if re.search(u"(.*mention.*|.*返信.*)", params["text"]) is not None:
      sc.rtm_send_message(channel, "<@" + params["user"] + "> " + u"@とSlackのIDを付けることでメンション(リプライ)メッセージが作れるよ!")

  # Sleep Message of Bot.
  def sleep_message(self, sc, params, heroku_time, channel):
    sc.rtm_send_message(channel, "<@" + params["user"] + "> " + u"今日はもう休むよ!おやすみ!")
    time.sleep(heroku_time)
    sc.rtm_send_message(channel, u"おはよ!今日も1日頑張るよ!")
  #######################

  # connection error of Slack.
  def error_message(self, error):
    print(error)
    sys.exit()
  ############################
sbm = SlackHelpBot()