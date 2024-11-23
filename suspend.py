import re
from datetime import time
import paramiko
import const
import requests


def connectSsh(self,usr,pwd):
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(
        str(self),
        username=usr,
        password=pwd,
        look_for_keys=False,
        allow_agent=False)
    return conn

class Suspend:
    def voiceSuspend(self):
        try:
            const.loggersus.info(self['LOGREF'] + "  " + "Start Suspend: =========================================================================")
            const.loggersus.info(self['LOGREF'] + "  " + str(self))

            if self['ORDER_TYPE'] == 'MODI-PARTIAL SUSPEND':

                xmlfile = open('files/BAR_OUTGOING_CALL.xml', 'r')
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
                                      'LOGREF'] + "  " + "End Suspend: =========================================================================")
                return str(ResultCode[0])

            if self['ORDER_TYPE'] == 'SUSPEND':
                xmlfile = open('files/BAR_OUTGOING_CALL.xml', 'r')
                data = xmlfile.read()

                for key in self:
                    value = self[key]
                    data = data.replace(key, str(value))

                response = requests.request("POST", const.voiceend, data=data)

                const.loggersus.info(self['LOGREF'] + "  " + str(response.request.body))
                const.loggersus.info(self['LOGREF'] + "  " + "Response Outgoing Bar: =================================")
                const.loggersus.info(self['LOGREF'] + "  " + str(response.text))

                ResultCode = re.findall("<ns1:ResultCode>(.*?)</ns1:ResultCode>", str(response.content))
                ResultDesc = re.findall("<ns1:ResultDesc>(.*?)</ns1:ResultDesc>", str(response.content))

                const.loggersus.info(self['LOGREF'] + "  " + str(ResultCode[0]) + '#' + str(ResultDesc[0]))

                if ResultCode[0] == '0':

                    xmlfile = open('files/BAR_INCOMING_CALL.xml', 'r')
                    datainc = xmlfile.read()

                    for key in self:
                        value = self[key]
                        datainc = datainc.replace(key, str(value))

                    responseinc = requests.request("POST", const.voiceend, data=datainc)

                    const.loggersus.info(self['LOGREF'] + "  " + str(responseinc.request.body))
                    const.loggersus.info(
                        self['LOGREF'] + "  " + "Response Incoming Bar: =================================")
                    const.loggersus.info(self['LOGREF'] + "  " + str(responseinc.text))

                    ResultCodeinc = re.findall("<ns1:ResultCode>(.*?)</ns1:ResultCode>", str(responseinc.content))
                    ResultDescinc = re.findall("<ns1:ResultDesc>(.*?)</ns1:ResultDesc>", str(responseinc.content))

                    result = Suspend.crbt(self)

                    const.loggersus.info(self['LOGREF'] + "  " + str(ResultCodeinc[0]) + '#' + str(ResultDescinc[0])+ '#' + str(result))

                    return str(ResultCodeinc[0])
                    const.loggersus.info(self['LOGREF'] + "  " + "End Suspend: =========================================================================")

                else:

                    const.loggersus.info(self['LOGREF'] + "  " + "End Suspend: =========================================================================")
                    return str(ResultCode[0])

        except Exception as e:
            const.loggersus.error(self['LOGREF'] + "  " + str(e))
            const.loggersus.info(self['LOGREF'] + "  " + "End Suspend: =========================================================================")
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

    def broadbandSuspend(self):

        #LDAP
        desc= ""
        conn = connectSsh(const.claip, const.clauser, const.clapwd)
        #stdin, stdout, stderr = conn.exec_command("ldapsearch -h "+const.ldapip+" -D \"uid="+const.ldapid+",cn=config\" -w "+const.ldappwd+" -b \"ou=people,o=auth\" uid="+self['TPNO']+"")
        remote_conn = conn.invoke_shell()
        remote_conn.send("/clarity/c12app1/etc/ldaprunit.sh /clarity/c12app1/ldapbin/ldapmodify \n")
        remote_conn.send("""dn: uid="""+self['TPNO']+""", ou=people, o=auth
        changetype: modify
        replace: sltInactiveStatus
        sltInactiveStatus: Suspended
        -
        replace: inetUserStatus
        inetUserStatus: inactive
        -
        add: description
        description: """+desc+"""
        
        \n""")

        remote_conn.send("\n")
        time.sleep(2)
        output = remote_conn.recv(10000)
        print(output.decode("utf-8"))

        #PCRF

    def iptvSuspend(self):
        try:
            const.loggersus.info(self['LOGREF'] + "  " + "Start Suspend: =========================================================================")
            const.loggersus.info(self['LOGREF'] + "  " + str(self))

            xmlfile = open('files/IPTV_SUNT_SUSPEND.xml', 'r')
            data = xmlfile.read()

            for key in self:
                value = self[key]
                data = data.replace(key, str(value))

            response = requests.request("POST", const.iptvend, data=data)

            const.loggersus.info(self['LOGREF'] + "  " + str(response.request.body))
            const.loggersus.info(self['LOGREF'] + "  " + "Response : =================================")
            const.loggersus.info(self['LOGREF'] + "  " + str(response.text))

            Result = re.findall("<ax225:abstractServiceObjects xsi:type=\"ax222:AbstractServiceObject\">(.*?)</ax225:abstractServiceObjects>", str(response.content))
            ResultCode = re.findall("<ax222:value>(.*?)</ax222:value>", str(Result[0]))
            ResultDesc = re.findall("<ax222:value>(.*?)</ax222:value>", str(Result[1]))


            const.loggersus.info(self['LOGREF'] + "  " + str(ResultCode[0]) + '#' + str(ResultDesc[0]))
            const.loggersus.info(self[
                                  'LOGREF'] + "  " + "End Suspend: =========================================================================")
            return str(ResultCode[0])


        except Exception as e:
            const.loggersus.error(self['LOGREF'] + "  " + str(e))
            const.loggersus.info(self['LOGREF'] + "  " + "End : =========================================================================")
            return str(e)