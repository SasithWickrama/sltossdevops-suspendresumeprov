from log import getLogger

voiceend = 'http://10.68.128.3:8080/spg'
crbt= 'http://10.68.198.66/SLTCrbt/ProvisionCallback.php'
iptvend='http://172.25.16.42:8082/tbms/services/TPEWebService.TPEWebServiceHttpSoap11Endpoint/'

dbhost='172.25.1.172'
dbport=1521
dbservice='clty'
dbuser='OSSPRG'
dbpwd='prgoss456'


loggersus = getLogger('susprov', 'logs/susprov')
loggerres = getLogger('resprov', 'logs/resprov')