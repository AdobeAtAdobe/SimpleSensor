'''
Main config loader
'''

from simplesensor.shared.threadsafeLogger import ThreadsafeLogger
import configparser
import os.path
import json

baseConfig = {}
configParser = configparser.ConfigParser()
configFilePath = None

def load(loggingQueue, name):
    """ Build dictionary of config values, return it """
    logger = ThreadsafeLogger(loggingQueue, '{0}-{1}'.format(name, 'ConfigLoader'))

    load_base(logger)
    # load_secrets(logger)
    return baseConfig

def load_secrets(logger):
    """ Load secrets.conf into baseConfig"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'config', 'secrets.conf')) as f:
            configParser.read_file(f)
            configFilePath = "/secrets.conf"
    except IOError:
        configParser.read(os.path.join(os.path.dirname(__file__),"./config/secrets.conf"), 'utf8')
        configFilePath = os.path.join(os.path.dirname(__file__),"./config/secrets.conf")
        exit

def load_base(logger):
    """ Load base.conf into baseConfig"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'config', 'base.conf')) as f:
            configParser.read_file(f)
            configFilePath = "./config/base.conf"
    except Exception as e:
        print('Error loading base config: ', e)
        configParser.read(os.path.join(os.path.dirname(__file__),"./config/base.conf"), 'utf8')
        configFilePath = os.path.join(os.path.dirname(__file__),"./config/base.conf")
        exit

    """Test mode"""
    try:
        TEST_MODE=configParser.getboolean('BaseConfig','test_mode')
    except:
        TEST_MODE = False
    logger.info("Test mode is set to : %s" % TEST_MODE)
    baseConfig['TestMode'] = TEST_MODE

    """ Default log directory """
    try:
        log_dir=configParser.get('BaseConfig','default_log')
    except:
        log_dir = "~/simplesensor_logs/app.log"
    logger.info("Default log directory is set to : %s" % log_dir)
    baseConfig['DefaultLog'] = log_dir

    ################ MODULES ################

    try:
        strVal = configParser.get('BaseConfig', 'collection_modules')
        val = json.loads(strVal)
    except Exception as e:
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
