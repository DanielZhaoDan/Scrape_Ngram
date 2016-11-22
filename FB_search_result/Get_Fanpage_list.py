import re
import urllib2

cookie = 'datr=OYmDV4pQ1woh4694JL3-5EoE; _ga=GA1.2.905364245.1476499425; sb=ZYmDVwozRepnSPcjn8-p-9Ul; pl=n; lu=gg-TFkXk6ygDB3WFT8S3NQgw; c_user=100006957738125; xs=196%3AZqliNb7ajY5nOw%3A2%3A1477666718%3A20772; fr=1pJP65hZ44wMFk9by.AWW44F9g-ph48sUmf7MsykLo628.BXg4k5.ss.FgT.0.0.BYNC-4.AWX3s7bH; csm=2; s=Aa5x7GMcTBJohGaj.BYE2ef; p=-2; presence=EDvF3EtimeF1479815214EuserFA21B06957738125A2EstateFDt2F_5b_5dElm2FnullEuct2F147981449B0EtrFnullEtwF1591607096EatF1479815201758G479815214722CEchFDp_5f1B06957738125F5CC'

def get_fan_param(ori):
    ori = unicode(ori, 'unicode-escape').replace("\\","").replace("&quot;","").replace("&#039;","'")
    reg = '"_2kcr _42ef".*?onmouseover="LinkshimAsyncLink.swap\(this, (.*?)\)'
    if '"_2kcr _42ef"' in ori:
        res = re.compile(reg).findall(ori)
        if(len(res)>0):
            return str(res[0])
    return "N/A"

def request_html(url):
    req = urllib2.Request(url)
    req.add_header("Cookie",cookie)
    req.add_header("user-agent","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)")
    req.add_header("accept", "*/*")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return res

def read_from_file(filename):
    file = open(filename)
    data = []

    i=0

    while 1:
        line = file.readline()
        if not line:
            break
        params = line.split(" ")
        is_fan_param = "N/A"
        if "Y" in params[1]:
            try:
                is_fan_param = get_fan_param(request_html(params[0]))
            except:
                is_fan_param = 'N/A'
        one_row = is_fan_param+'\r'
        print(one_row)
        data.append(one_row)
        i+=1
        if i%1000==0:
            write_list_to_file(data, 'out'+str(i)+'.txt')
            data = []
    write_list_to_file(data, 'out'+str(i)+'.txt')

def write_list_to_file(data, filename):
    f=file(filename,"w+")
    f.writelines(data)
    f.close();

read_from_file('in/Singapore-Bali.txt')


