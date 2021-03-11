import sys

serv = []           # 服务器
vm = {}             # 虚拟机
req = []            # 请求
days = 0


def readdata():
    global days
    serv_num = int(sys.stdin.readline())
    print(serv_num)
    for i in range(serv_num):
        line = sys.stdin.readline()[1:-2].split(',')
        line[1] = int(line[1])
        line[2] = int(line[2])
        line[3] = int(line[3])
        line[4] = int(line[4])
        serv.append(line)
    for i in serv:
        print(i)
    vm_num = int(sys.stdin.readline())  # 读取虚拟机类型数量
    print(vm_num)
    for i in range(vm_num):
        line = sys.stdin.readline()[1:-2].split(',')
        line[1] = int(line[1])
        line[2] = int(line[2])
        line[3] = int(line[3])
        vm[line[0]] = line[1:]
    for i in vm:
        print(i)
    days = int(sys.stdin.readline())  # 读取请求天数T
    for i in range(days):
        day_req = []
        reqs = int(sys.stdin.readline())  # 当天的请求数量R
        for j in range(reqs):
            line = sys.stdin.readline()[1:-2].split(',')
            line[1] = line[1].lstrip()
            line[-1] = int(line[-1])
            day_req.append(line)
        req.append(day_req)
    for i in req:
        print(i)


def main():
    # to read standard input
    # process
    # to write standard output
    # sys.stdout.flush()




if __name__ == "__main__":
    main()
