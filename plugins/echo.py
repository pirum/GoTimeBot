import plugin
import re

class EchoPlugin(plugin.Plugin):
  
  def __init__(self, pluginRegistry):
    pluginRegistry.registerTrigger('echo:message', re.compile('echo .*'), self)
    
  def handleMessage(self, bot, triggerName, message):
    bot.say(message)