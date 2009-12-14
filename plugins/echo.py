import socrates
import re

class EchoPlugin(socrates.Plugin):
  
  def __init__(self, pluginRegistry):
    pluginRegistry.registerTrigger('echo:message', re.compile('echo .*'), self)
    
  def handleMessage(self, bot, triggerName, message):
    bot.say(message)