__author__ = 'arl'


from json import load
from sys import argv


PATH_CONF_CUCKOO = 'cuckoo'
PATH_REPORT = 'report'
PATH_BOOTSTRAP = 'bootstrap'


def make_hex_array(data):
    return ','.join(['0x%02x' % ord(x) + ('\r\n' if (i + 1) % 16 == 0 else '') for i, x in enumerate(data)])


def escape_file_data(data):
    data = data.replace("\\", "\\\\")
    data = data.replace("\"", "\\\"")
    dv = data.split('\n')
    data = ''
    for ds in dv:
        data += ds.rstrip() + '\\\r\n'

    return data


def read_data(fn):
    try:
        return open(fn, 'r').read()
    except Exception as e:
        print(f"File Read Exception: {e}")
        return


def write_data(fn, data):
    try:
        open(fn, 'w').write(data)
    except Exception as e:
        print(f'File Write Exception: {e}')
        return False

    return True


def get_file_data(conf, option):
    fn = conf.get(option, '')
    if not fn:
        print(f'Configuration parameter: {option} is absent')
        return False

    return read_data(fn)


def create_includes(conf):
    cuckoo_d = get_file_data(conf, PATH_CONF_CUCKOO)
    report_d = get_file_data(conf, PATH_REPORT)
    bootstrap_d = get_file_data(conf, PATH_BOOTSTRAP)

    # escape characters
    cuckoo_file = "static const char *cuckoo_conf = \"%s\";" % escape_file_data(cuckoo_d)
    report_file = "static const char *report_data = \"%s\";" % escape_file_data(report_d)
    bootstrap_file = "static const char bootstrap_data[] = {\r\n%s\r\n};" % make_hex_array(bootstrap_d)

    if not write_data("code_cuckoo.conf", cuckoo_file):
        return False
    if not write_data("data_report.html", report_file):
        return False
    if not write_data("data_bootstrap.css", bootstrap_file):
        return False

    return True


def read_conf(fn):
    try:
        return load(open(fn, 'r'))
    except Exception as e:
        print(f'Configuration Read Exception: %s') % e
        return


def main():
    if len(argv) < 2:
        print(f'GenDefaultData usage: {argv[0]} [config]')
        exit(1)

    conf = read_conf(argv[1])
    if not conf:
        exit(2)

    if not create_includes(conf):
        exit(3)


if __name__ == '__main__':
    main()
