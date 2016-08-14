# - *- coding: utf-8 -*
class TokenInput:
  def __init__(self, token=""):
    try:
      rfile = open("token.txt", "r")
      token = rfile.readline()
    except IOError:
      print("token.txt cannot be opened.")
      print("Please input of slack bot API token.")
      token = input('Token: ')
      wfile = open("token.txt", "w+")
      wfile.writelines(token)
      wfile.close
      self.token = token
    else:
      self.token = token
      rfile.close

  def info(self):
    return self.token