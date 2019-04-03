import json
import urllib
import re


def parse_resp(resp):
    reg = 'webFormContext":"(.*?)"},"head"'
    data = re.compile(reg).findall(resp)[0]
    webform_context_obj = json.loads(data)

    url = webform_context_obj['redirectUrl'] + '?'

    url_params = urllib.urlencode(webform_context_obj['params'])

    print url + url_params


def parse_webform_context():
    resp = '{"bizDate":null,"currentResultCode":null,"errorContext":{"errorStack":[],"thirdPartyError":""},"externalUserId":"dana_test_20181130_0005","isCreateBalanceAccount":"Y","success":true,"userId":"2164230001020175","userInfo":null,"webFormContext":"{\\"method\\":\\"GET\\",\\"params\\":{\\"clientId\\":\\"2018111401976741790344\\",\\"redirectUrl\\":\\"http://isupergw-eu95.dl.alipaydev.com/isupergw/dana22/dana229901.htm\\",\\"seamlessData\\":\\"{\\\\\\"mobile\\\\\\":\\\\\\"62-81813746203\\\\\\",\\\\\\"verifiedTime\\\\\\":\\\\\\"2001-07-04T12:08:56+05:30\\\\\\",\\\\\\"externalUid\\\\\\":\\\\\\"2164230001020175\\\\\\",\\\\\\"reqTime\\\\\\":\\\\\\"2018-11-30T13:57:27+08:00\\\\\\",\\\\\\"reqMsgId\\\\\\":\\\\\\"80eae3c0fa2f422da728720487d741e5\\\\\\"}\\",\\"requestId\\":\\"41c635043025471996a13f32e2311e3c\\",\\"seamlessSign\\":\\"U0aLeWVDTnUCnxofOIuydhRyNopuqKYVdQuhSYvvTlsb7sPF6F7hOrZzlVhMsjVk8mSVvIWj09ZGUfPrxPbO8Uawn7ERMoPaqR7K1Tnyv4UrA4qXeFYAYFdlAex3rvcQYP0Gimy7xRJx7PpKK4ZuaEj3LdPK5DepUNFaQIA48fD0KaVyzXyo1kMACLHMCyxjPRKkDIQ+s31lgvwS1wWswaihU8qe8trqUgJz9uvZ0hBjnj1X0oFf4MEyav97kmRA2Ayqk3dlnq4yeI0jEgcIwlfOoxSdbMSHPLxwBVQZ75Tqvmpm980l3AveOeRi7B4y6BqxT5eOEtUaF3fzvQPpLA==\\",\\"scopes\\":\\"DEFAULT_BASIC_PROFILE,AGREEMENT_PAY,QUERY_BALANCE,CASHIER,MINI_DANA,PUBLIC_ID,LAZADA_WALLET\\",\\"state\\":\\"2018112918031113000170000002796\\",\\"lang\\":\\"id-ID\\",\\"terminalType\\":\\"PC\\"},\\"redirectUrl\\":\\"http://aphome.id.devbranch3.alipay.net/m/portal/oauth\\",\\"webFormMethod\\":\\"REDIRECT\\"}"}'
    resp_obj = json.loads(resp)
    webform_context_obj = json.loads(resp_obj['webFormContext'])

    url = webform_context_obj['redirectUrl'] + '?'

    url_params = urllib.urlencode(webform_context_obj['params'])

    print url + url_params


resp = '{"response":{"body":{"externalUserId":"787718","isCreateBalanceAccount":"N","resultInfo":{"resultCode":"SUCCESS","resultCodeId":"00000000","resultMsg":"Success","resultStatus":"S"},"userId":"2164230000698142","webFormContext":"{\"method\":\"GET\",\"params\":{\"clientId\":\"2018111401976741790344\",\"redirectUrl\":\"http://isupergw-eu95-0.idgz00a.test.alipay.net/isupergw/dana22/dana229901.htm\",\"seamlessData\":\"{\\\"mobile\\\":\\\"62-8181374150\\\",\\\"verifiedTime\\\":\\\"2018-11-22T12:08:56+08:30\\\",\\\"externalUid\\\":\\\"2164230000698142\\\",\\\"reqTime\\\":\\\"2019-01-20T23:10:37-08:00\\\",\\\"reqMsgId\\\":\\\"7a1f3e83ad9f46eea0748142a637043f\\\"}\",\"requestId\":\"bfbefbe1e7c645a1aeb4b217efa1fad5\",\"seamlessSign\":\"Rg+qd8qL+888aMvbrYwVN92uMXKksFCPGgnD0fHUZJ/VNeXk9rYUlW/JIivmUEU2XW024L9aa62l07sdm2R7p44g1w0xIPl68skTUIf2lr8YfuJTYfAmFngNPeYUpIHHhqUxKh/wZ0PWqSzWfs0S2w+KzkoHIiFNwMqAVgWQDEp5N6E5Lun9w0lOvjJKX9Ime8mGUwcZokNMgrVZNTzcPZLr3YaUQM7sObmK0APwETYckDfZy2BU2pgwQZXFi5PWcmnPXXnFSBRB8G2cmwKzrE2yc0b5xv7aNos8V3fYTR96NNWC6isgFv3qAaBOD6hzSiNorSt6P34DDjPkXFw+KA==\",\"scopes\":\"DEFAULT_BASIC_PROFILE,AGREEMENT_PAY,QUERY_BALANCE,CASHIER,MINI_DANA,PUBLIC_ID,LAZADA_WALLET\",\"state\":\"2019012018031113000140000138307\",\"lang\":\"th-th\",\"terminalType\":\"APP\"},\"redirectUrl\":\"http://aphome-test3-dana.alipaydev.com/m/portal/oauth\",\"webFormMethod\":\"REDIRECT\"}"},"head":{"clientId":"4K00000010000002","function":"alipay.intl.user.register.registerUser","reqMsgId":"a1bd2fc7-1e67-4268-9148-9880f4c95ef5","respTime":"2019-01-20T23:10:37-08:00","version":"2.1.1"}},"signature":"BigjhVHHrBsGsHrWV7PNvAPyrWqwEHc0Hp/uqzfzIqFKmegI2bqJg67MCJNo4ikGEUojj7SNmPzb8WnBmk+7JMB5mFU4z41OdDHjoEzmTM+azpjubecZQAgTipgXxoN2OhkjuAVPNuuxBOm9PU0hA1AB1AoHIbBTX5GLkZcgrs1qard5HBnz8exe7gr78hbJpezukkz3FQRO3LXKA+SzFHm8/XrmikuoTkzF3b0Kgp9ACsJVNAcucEYePfRo0+yF3avO46DzItLfpG0UtgQHBcAaquXBusiCan2TXlxzvJYYT2nDad+Vz9b676WiOTwlQ9B4F+bK5lXJlgFzldPRGQ=="}'

parse_resp(resp)

# parse_webform_context()