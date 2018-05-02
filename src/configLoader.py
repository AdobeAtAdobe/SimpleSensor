'''
Main config loader
'''
import configparser
import os.path
import json

baseConfig = {}
configParser = configparser.ConfigParser()
configFilePath = None

def load(logger):
    """ Build dictionary of config values, return it """
    loadBase(logger)
    loadSecrets(logger)
    return baseConfig

def loadSecrets(logger):
    """ Load secrets.conf into baseConfig"""
    try:
        with open("/secrets.conf") as f:
            configParser.readfp(f)
            configFilePath = "/secrets.conf"
    except IOError:
        configParser.read(os.path.join(os.path.dirname(__file__),"config/secrets.conf"))
        configFilePath = os.path.join(os.path.dirname(__file__),"config/secrets.conf")
        exit

def loadBase(logger):
    """ Load base.conf into baseConfig"""
    try:
        with open("/base.conf") as f:
            configParser.readfp(f)
            configFilePath = "/base.conf"
    except IOError:
        configParser.read(os.path.join(os.path.dirname(__file__),"config/base.conf"))
        configFilePath = os.path.join(os.path.dirname(__file__),"config/base.conf")
        exit

    """Test mode"""
    try:
        TEST_MODE=configParser.getboolean('BaseConfig','test_mode')
    except:
        TEST_MODE = False
    logger.info("Test mode is set to : %s" % TEST_MODE)
    baseConfig['TestMode'] = TEST_MODE


    ################ MODULES ################

    try:
        strVal = configParser.get('BaseConfig', 'collection_modules')
        val = json.loads(strVal)
    except:
        strVal = 'camCollectionPoint'
        val = [strVal]
    baseConfig['CollectionModules'] = val
    logger.info("Collection point modules to use : %s" % strVal)

    try:
        strVal = configParser.get('BaseConfig', 'communication_modules')
        val = json.loads(strVal)
    except:
        strVal = 'websocketServer'
        val = [strVal]
    baseConfig['CommunicationModules'] = val
    logger.info("Communication method modules to use : %s" % strVal)

    logger.info("App config for base done")

    return baseConfig