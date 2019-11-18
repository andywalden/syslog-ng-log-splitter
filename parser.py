import re

class LogSplitter(object):

    def parse(self, log):
        long_log = re.compile(r'Trace route attack')
        if long_log.search(log['MESSAGE'].decode('utf-8')):
            self.split_log(log['MESSAGE'].decode('utf-8'))
            return False
        else:
            return True

    def split_log(self, log):
        print(log)
        re_first_part = re.compile(r'.+?(?=ip\=)')
        re_last_part = re.compile(r' begin time.*')
        try:
            first_part = re_first_part.match(log).group()
            last_part = re_last_part.search(log).group()
        except AttributeError:
            return True
        ip_pairs = self.parse_ip_pairs(log)

        logs = []
        for pair in ip_pairs:
            logs.append(''.join([first_part, pair, last_part, '\n']))
        self.write_logs(logs)

    def parse_ip_pairs(self, log):
        ip_pairs = re.compile(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}->\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}')
        return ip_pairs.findall(log)

    def write_logs(self, logs):
        with open('/var/log/parsed-logs', 'a') as f:
            for log in logs:
                f.write(log)
