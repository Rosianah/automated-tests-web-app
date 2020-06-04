from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")

Telegraminfo = config_object['TELEGRAMINFO']
api_hash = format(Telegraminfo["api_hash"])
print(api_hash)
