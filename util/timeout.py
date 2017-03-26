import re
import signal


def extract_data_with_timeout_control(time_out, reg, html):
    def handler():
        raise AssertionError

    try:
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(time_out)
        params_list = re.compile(reg).findall(html)
        return params_list
    except AssertionError:
        print 'timeout'
        return []

if __name__ == '__main__':
    print extract_data_with_timeout_control(6, r'xxx(.*?)o', 'hello, hi, heqqqqqo, hhed')