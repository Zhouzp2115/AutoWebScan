import sys

def split(data):
    index = 0
    while data[index] != ' ':
        index += 1
    domain = data[0:index]
    ips = data[index:len(data)]
    ips = ips.replace('\n', '')
    ips = ips.split(',')
    return domain, ips


def getIpDomain(fileName):
    file = open(fileName)
    domains = []
    ips = []
    while True:
        line = file.readline()
        if line == '':
            file.close()
            break
        else:
            domain, ip = split(line)
            domains.append(domain)
            for item in ip:
                item = item.lstrip().rstrip()
                if item not in ips:
                    ips.append(item)

    return domains, ips


if __name__ == '__main__':
    fileName = sys.argv[1]

    domains, ips = getIpDomain(fileName)
    print(domains)
    print(ips)

    file = open(fileName + '.domain', 'w+')
    for domain in domains:
        file.write(domain + ',to_scan' + '\n')
