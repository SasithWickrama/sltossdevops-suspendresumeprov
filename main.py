import multiprocessing
import random
import sys
from datetime import datetime

import db
from suspend import Suspend
from resume import Resume

conn = db.DbConnection.dbconnPrg("")
cmonth = datetime.now().strftime('%Y%m')
data = {}


def specific_string(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    # define the condition for random string
    return ''.join((random.choice(sample_string)) for x in range(length))


def suspend(typ, x):
    if typ == 'VOICE':
        sql = 'select ROWID,ORDER_TYPE ,CCT,STATUS ' \
              'from  EXPROV_VOICE_' + cmonth + ' where STATUS = 0 AND ORDER_TYPE IN (\'MODI-PARTIAL SUSPEND\',\'SUSPEND\') ' \
                                               'AND MOD(DBMS_ROWID.ROWID_ROW_NUMBER(EXPROV_VOICE_' + cmonth + '.ROWID), 5) = ' + str(
            x)
    if typ == 'BB':
        sql = 'select ROWID,ORDER_TYPE ,CCT,STATUS ' \
              'from  EXPROV_BB_' + cmonth + ' where STATUS = 0 AND ORDER_TYPE IN (\'MODI-PARTIAL SUSPEND\',\'SUSPEND\') ' \
                                            'AND MOD(DBMS_ROWID.ROWID_ROW_NUMBER(EXPROV_BB_' + cmonth + '.ROWID), 5) = ' + str(
            x)
    if typ == 'IPTV':
        sql = 'select ROWID,ORDER_TYPE ,CCT,STATUS ' \
              'from  EXPROV_IPTV_' + cmonth + ' where STATUS = 0 AND ORDER_TYPE IN (\'MODI-PARTIAL SUSPEND\',\'SUSPEND\') ' \
                                              'AND MOD(DBMS_ROWID.ROWID_ROW_NUMBER(EXPROV_IPTV_' + cmonth + '.ROWID), 5) = ' + str(
            x)

    c = conn.cursor()
    c.execute(sql)

    for row in c:
        ROWID, ORDER_TYPE, CCT, STATUS = row

        data['ROWID'] = ROWID
        data['ORDER_TYPE'] = ORDER_TYPE
        data['TPNO'] = CCT[1:10]
        data['STATUS'] = STATUS
        data['MSISDN'] = CCT
        data['STAT'] = 2

        refid = specific_string(15)
        data['LOGREF'] = refid

        print(data)

        if typ == 'VOICE':
            result = Suspend.voiceSuspend(data)
            if result == '0':
                sqlupdate = 'update EXPROV_VOICE_' + cmonth + ' set STATUS=:STATUS, STATUS_DATE=sysdate where  ROWID= :ROW_ID and STATUS=0'
                with conn.cursor() as cursor2:
                    cursor2.execute(sqlupdate, [100, ROWID])
                    conn.commit()
                    print(cursor2.rowcount)
            else:
                sqlupdate = 'update EXPROV_VOICE_' + cmonth + ' set STATUS=:STATUS,STATUS_DATE=sysdate where  ROWID= :ROW_ID and STATUS=0'
                with conn.cursor() as cursor2:
                    cursor2.execute(sqlupdate, [200, ROWID])
                    conn.commit()
                    print(cursor2.rowcount)

        if typ == 'BB':
            result = Suspend.broadbandSuspend()
            if result == '0':
                sqlupdate = 'update EXPROV_BB_' + cmonth + ' set STATUS=:STATUS, STATUS_DATE=sysdate where  ROWID= :ROW_ID and STATUS=0'
                with conn.cursor() as cursor2:
                    cursor2.execute(sqlupdate, [100, ROWID])
                    conn.commit()
                    print(cursor2.rowcount)
            else:
                sqlupdate = 'update EXPROV_BB_' + cmonth + ' set STATUS=:STATUS,STATUS_DATE=sysdate where  ROWID= :ROW_ID and STATUS=0'
                with conn.cursor() as cursor2:
                    cursor2.execute(sqlupdate, [200, ROWID])
                    conn.commit()
                    print(cursor2.rowcount)

        if typ == 'IPTV':
            result = Suspend.iptvSuspend()
            if result == 'Success':
                sqlupdate = 'update EXPROV_IPTV_' + cmonth + ' set STATUS=:STATUS, STATUS_DATE=sysdate where  ROWID= :ROW_ID and STATUS=0'
                with conn.cursor() as cursor2:
                    cursor2.execute(sqlupdate, [100, ROWID])
                    conn.commit()
                    print(cursor2.rowcount)
            else:
                sqlupdate = 'update EXPROV_IPTV_' + cmonth + ' set STATUS=:STATUS,STATUS_DATE=sysdate where  ROWID= :ROW_ID and STATUS=0'
                with conn.cursor() as cursor2:
                    cursor2.execute(sqlupdate, [200, ROWID])
                    conn.commit()
                    print(cursor2.rowcount)


def resume(typ, x):
    if typ == 'VOICE':
        sql = 'select ROWID,ORDER_TYPE ,CCT,STATUS ' \
              'from  EXPROV_VOICE_' + cmonth + ' where STATUS = 0 AND ORDER_TYPE IN (\'MODI-PARTIAL RESUME\',\'RESUME\') ' \
                                               'AND MOD(DBMS_ROWID.ROWID_ROW_NUMBER(EXPROV_VOICE_' + cmonth + '.ROWID), 5) = ' + str(
            x)
        if typ == 'BB':
            sql = 'select ROWID,ORDER_TYPE ,CCT,STATUS ' \
                  'from  EXPROV_BB_' + cmonth + ' where STATUS = 0 AND ORDER_TYPE IN (\'MODI-PARTIAL RESUME\',\'RESUME\') ' \
                                                'AND MOD(DBMS_ROWID.ROWID_ROW_NUMBER(EXPROV_BB_' + cmonth + '.ROWID), 5) = ' + str(
                x)
        if typ == 'IPTV':
            sql = 'select ROWID,ORDER_TYPE ,CCT,STATUS ' \
                  'from  EXPROV_IPTV_' + cmonth + ' where STATUS = 0 AND ORDER_TYPE IN (\'MODI-PARTIAL RESUME\',\'RESUME\') ' \
                                                  'AND MOD(DBMS_ROWID.ROWID_ROW_NUMBER(EXPROV_IPTV_' + cmonth + '.ROWID), 5) = ' + str(
                x)

    c = conn.cursor()
    c.execute(sql)

    for row in c:
        ROWID, ORDER_TYPE, CCT, STATUS = row

        data['ROWID'] = ROWID
        data['ORDER_TYPE'] = ORDER_TYPE
        data['TPNO'] = CCT[1:10]
        data['STATUS'] = STATUS
        data['MSISDN'] = CCT
        data['STAT'] = 3

        refid = specific_string(15)
        data['LOGREF'] = refid

        print(data)

        if typ == 'VOICE':
            result = Resume.voiceResume(data)
            if result == '0':
                sqlupdate = 'update EXPROV_VOICE_' + cmonth + ' set STATUS=:STATUS, STATUS_DATE=sysdate where  ROWID= :ROW_ID and STATUS=0'
                with conn.cursor() as cursor2:
                    cursor2.execute(sqlupdate, [100, ROWID])
                    conn.commit()
                    print(cursor2.rowcount)
            else:
                sqlupdate = 'update EXPROV_VOICE_' + cmonth + ' set STATUS=:STATUS,STATUS_DATE=sysdate where  ROWID= :ROW_ID and STATUS=0'
                with conn.cursor() as cursor2:
                    cursor2.execute(sqlupdate, [200, ROWID])
                    conn.commit()
                    print(cursor2.rowcount)

        if typ == 'BB':
            result = Resume.broadbandResume(data)
            if result == '0':
                sqlupdate = 'update EXPROV_BB_' + cmonth + ' set STATUS=:STATUS, STATUS_DATE=sysdate where  ROWID= :ROW_ID and STATUS=0'
                with conn.cursor() as cursor2:
                    cursor2.execute(sqlupdate, [100, ROWID])
                    conn.commit()
                    print(cursor2.rowcount)
            else:
                sqlupdate = 'update EXPROV_BB_' + cmonth + ' set STATUS=:STATUS,STATUS_DATE=sysdate where  ROWID= :ROW_ID and STATUS=0'
                with conn.cursor() as cursor2:
                    cursor2.execute(sqlupdate, [200, ROWID])
                    conn.commit()
                    print(cursor2.rowcount)

        if typ == 'IPTV':
            result = Resume.iptvResume(data)
            if result == 'Success':
                sqlupdate = 'update EXPROV_IPTV_' + cmonth + ' set STATUS=:STATUS, STATUS_DATE=sysdate where  ROWID= :ROW_ID and STATUS=0'
                with conn.cursor() as cursor2:
                    cursor2.execute(sqlupdate, [100, ROWID])
                    conn.commit()
                    print(cursor2.rowcount)
            else:
                sqlupdate = 'update EXPROV_IPTV_' + cmonth + ' set STATUS=:STATUS,STATUS_DATE=sysdate where  ROWID= :ROW_ID and STATUS=0'
                with conn.cursor() as cursor2:
                    cursor2.execute(sqlupdate, [200, ROWID])
                    conn.commit()
                    print(cursor2.rowcount)


if __name__ == '__main__':
    processes = []

    if sys.argv[1] == 'SUSPEND':
        for i in range(0, 5):
            if sys.argv[2] == 'VOICE':
                p = multiprocessing.Process(target=suspend, args=('VOICE', i,))

            if sys.argv[2] == 'BB':
                p = multiprocessing.Process(target=suspend, args=('BB', i,))

            if sys.argv[2] == 'IPTV':
                p = multiprocessing.Process(target=suspend, args=('IPTV', i,))

            processes.append(p)
            p.start()

    if sys.argv[1] == 'RESUME':
        for i in range(0, 5):
            if sys.argv[2] == 'VOICE':
                p = multiprocessing.Process(target=resume, args=('VOICE', i,))

            if sys.argv[2] == 'BB':
                p = multiprocessing.Process(target=resume, args=('BB', i,))

            if sys.argv[2] == 'IPTV':
                p = multiprocessing.Process(target=resume, args=('IPTV', i,))

            processes.append(p)
            p.start()

    # multiprocessing_func(i)
    for process in processes:
        process.join()
