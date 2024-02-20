import datetime

TXT_LOG = 'history.log'

def WriteLog(name,type,Message):#LOG書き込み関数
    now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    f = open(TXT_LOG, 'a')
    f.write(f'{now} || {type.ljust(10)}| {Message.ljust(40)}| {name}\n')
    f.close()
