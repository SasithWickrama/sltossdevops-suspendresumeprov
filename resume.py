import re
from datetime import time
import paramiko
import const
import requests


class Resume:
    def voiceResume(self):
        try:
            const.loggersus.info(self['LOGREF'] + "  " + "Start Resume: =========================================================================")
            const.loggersus.info(self['LOGREF'] + "  " + str(self))

            if self['ORDER_TYPE'] == 'MODI-PARTIAL RESUME':

                xmlfile = open('files/REMOVE_OGB.xml', 'r')
                data = xmlfile.read()

                for key in self:
                    value = self[key]
                    data = data.replace(key, str(value))

                response = requests.request("POST", const.voiceend, data=data)

                const.loggersus.info(self['LOGREF'] + "  " + str(response.request.body))
                const.loggersus.info(self['LOGREF'] + "  " + "Response : =================================")
                const.loggersus.info(self['LOGREF'] + "  " + str(response.text))

                ResultCode = re.findall("<ns1:ResultCode>(.*?)</ns1:ResultCode>", str(response.content))
                ResultDesc = re.findall("<ns1:ResultDesc>(.*?)</ns1:ResultDesc>", str(response.content))

                const.loggersus.info(self['LOGREF'] + "  " + str(ResultCode[0]) + '#' + str(ResultDesc[0]))
                const.loggersus.info(self[
                                         'LOGREF'] + "  " + "End Resume: =========================================================================")
                return str(ResultCode[0])

            if self['ORDER_TYPE'] == 'RESUME':
                xmlfile = open('files/REMOVE_OGB.xml', 'r')
                data = xmlfile.read()

                for key in self:
                    value = self[key]
                    data = data.replace(key, str(value))

                response = requests.request("POST", const.voiceend, data=data)

                const.loggersus.info(self['LOGREF'] + "  " + str(response.request.body))
                const.loggersus.info(self['LOGREF'] + "  " + "Response Outgoing Remove: =================================")
                const.loggersus.info(self['LOGREF'] + "  " + str(response.text))

                ResultCode = re.findall("<ns1:ResultCode>(.*?)</ns1:ResultCode>", str(response.content))
                ResultDesc = re.findall("<ns1:ResultDesc>(.*?)</ns1:ResultDesc>", str(response.content))

                const.loggersus.info(self['LOGREF'] + "  " + str(ResultCode[0]) + '#' + str(ResultDesc[0]))

                if ResultCode[0] == '0':

                    xmlfile = open('files/REMOVE_ICB.xml', 'r')
                    datainc = xmlfile.read()

                    for key in self:
                        value = self[key]
                        datainc = datainc.replace(key, str(value))

                    responseinc = requests.request("POST", const.voiceend, data=datainc)

                    const.loggersus.info(self['LOGREF'] + "  " + str(responseinc.request.body))
                    const.loggersus.info(
                        self['LOGREF'] + "  " + "Response Incoming Remove: =================================")
                    const.loggersus.info(self['LOGREF'] + "  " + str(responseinc.text))

                    ResultCodeinc = re.findall("<ns1:ResultCode>(.*?)</ns1:ResultCode>", str(responseinc.content))
                    ResultDescinc = re.findall("<ns1:ResultDesc>(.*?)</ns1:ResultDesc>", str(responseinc.content))

                    result = Resume.crbt(self)

                    const.loggersus.info(self['LOGREF'] + "  " + str(ResultCodeinc[0]) + '#' + str(ResultDescinc[0])+ '#' + str(result))

                    return str(ResultCodeinc[0])
                    const.loggersus.info(self['LOGREF'] + "  " + "End Resume: =========================================================================")

                else:

                    const.loggersus.info(self['LOGREF'] + "  " + "End Resume: =========================================================================")
                    return str(ResultCode[0])

        except Exception as e:
            const.loggersus.error(self['LOGREF'] + "  " + str(e))
            const.loggersus.info(self['LOGREF'] + "  " + "End Resume: =========================================================================")
            return str(e)

    def crbt(self):
        try:
            xmlfile = open('files/CallBackStatus.xml', 'r')
            headers= {'content-type':'text/xml'}
            data = xmlfile.read()

            for key in self:
                value = self[key]

                data = data.replace(key, str(value))

            response = requests.request("POST", const.crbt,headers=headers, data=data)
            const.loggersus.info(self['LOGREF'] + "  " + str(response.request.body))
            const.loggersus.info(self['LOGREF'] + "  " + "Response CRBT: =================================")
            const.loggersus.info(self['LOGREF'] + "  " + str(response.text))

            ResultCode = re.findall("<return xsi:type=\"xsd:string\">(.*?)</return>", str(response.content))
            return ResultCode[0]

        except Exception as e:
            const.loggersus.error(self['LOGREF'] + "  " + str(e))
            const.loggersus.info(self[
                                     'LOGREF'] + "  " + "End  : =========================================================================")
            return str(e)

    def broadbandResume(self):
        print(2)

    def iptvResume(self):
        try:
            const.logger.info(self['LOGREF'] + "  " + "Start Resume: =========================================================================")
            const.logger.info(self['LOGREF'] + "  " + str(self))

            xmlfile = open('files/IPTV_SUNT_RESUME.xml', 'r')
            data = xmlfile.read()

            for key in self:
                value = self[key]
                data = data.replace(key, str(value))

            response = requests.request("POST", const.iptvend, data=data)

            const.logger.info(self['LOGREF'] + "  " + str(response.request.body))
            const.logger.info(self['LOGREF'] + "  " + "Response : =================================")
            const.logger.info(self['LOGREF'] + "  " + str(response.text))

            Result = re.findall("<ax225:abstractServiceObjects xsi:type=\"ax222:AbstractServiceObject\">(.*?)</ax225:abstractServiceObjects>", str(response.content))
            ResultCode = re.findall("<ax222:value>(.*?)</ax222:value>", str(Result[0]))
            ResultDesc = re.findall("<ax222:value>(.*?)</ax222:value>", str(Result[1]))


            const.logger.info(self['LOGREF'] + "  " + str(ResultCode[0]) + '#' + str(ResultDesc[0]))
            const.logger.info(self[
                                  'LOGREF'] + "  " + "End Resume: =========================================================================")
            return str(ResultCode[0])


        except Exception as e:
            const.logger.error(self['LOGREF'] + "  " + str(e))
            const.logger.info(self['LOGREF'] + "  " + "End Resume: =========================================================================")
            return str(e)