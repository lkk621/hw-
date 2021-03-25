# -*- coding:utf-8 -*-
"""
作者：l50017479
日期：2021年03月25日
1585055345
71s
"""
import time
import sys

serv = []           # 服务器
serv_dict = {}
vm = {}             # 虚拟机
Reqs = []            # 请求
Days = 0
Arg1 = 0.6
Arg2 = 0.4
Day_needs = []       # 每一天的CPU和RAM需求


def value_rd(v1, v2, r):
    if abs(v1-v2) <= r and (v1 >= 1 and v2 >= 1 or v1 < 1 and v2 < 1):
        return True
    return False


def readdata():
    global Days
    global Arg1
    global Arg2
    serv_num = int(sys.stdin.readline())
    for i in range(serv_num):
        line = sys.stdin.readline()[1:-2].split(',')
        line[1] = int(line[1])
        line[2] = int(line[2])
        line[3] = int(line[3])
        line[4] = int(line[4])
        line.append(round(line[1] / line[2], 1))
        serv.append(line)
    serv.sort(key=lambda x: (x[3] + x[4])//(x[1]*Arg1 + x[2]*Arg2))
    for ser in serv:
        serv_dict[ser[0]] = ser[1:]
    vm_num = int(sys.stdin.readline().rstrip('\n'))  # 读取虚拟机类型数量
    for i in range(vm_num):
        line = sys.stdin.readline()[1:-2].split(',')
        line[1] = int(line[1])
        line[2] = int(line[2])
        line[3] = int(line[3])
        line.append(round(line[1] / line[2], 1))
        vm[line[0]] = line[1:]
    Days = int(sys.stdin.readline())  # 读取请求天数T
    for i in range(Days):
        day_req = []
        reqs = int(sys.stdin.readline().rstrip('\n'))  # 当天的请求数量R
        day_need_cpu = 0
        day_need_ram = 0
        for j in range(reqs):
            line = sys.stdin.readline()[1:-2].split(',')
            line[1] = line[1].lstrip()
            line[-1] = int(line[-1])
            day_req.append(line)
            if line[0] == 'add':
                day_need_cpu += vm[line[1]][0]
                day_need_ram += vm[line[1]][1]
        Day_needs.append([day_need_cpu, day_need_ram])
        Reqs.append(day_req)


def main():
    readdata()                  # 读取数据
    serv_poll = {}              # 已购买的服务器
    host = {}                   # 存放申请虚拟机的主机信息
    NUM = 0                     # 服务器编号
    NUM_VM = 0                  # 已部署的vm
    servers = {}  # 记录服务器部署虚机的信息， # servers = {服务器ID：[主机...]}
    for i in range(Days):
        serv.sort(key=lambda x: (x[3] + x[4])*(Days-i) // (x[1] * Arg1 + x[2] * Arg2))
        # print(serv)
        day_serv = []
        day_serv_kind = {}
        # 对当前crr匹配度不高的虚拟机进行扩容迁移   CPU，RAM比率
        # host = {主机号：[虚拟机类型，服务器ID，节点]}
        # serv_poll = {ID：[型号，两个节点的资源]}
        # vm = {类型：[CPU，RAM，单双，crr]}

        # 迁移虚拟机
        day_move = {}           # {主机：目的服务器}

        # 处理当天请求
        # serv_poll[NUM] = [ser[0], ser[1] / 2, ser[2] / 2, ser[1] / 2, ser[2] / 2]
        for req in Reqs[i]:
            flag = 0            # 如果当前请求满足了，则flag置为1，否则为0，需要扩容服务器
            if req[0] == 'add':
                for k, v in serv_poll.items():
                    if vm[req[1]][2] == 1:                      # 双节点部署
                        if v[1] >= vm[req[1]][0]/2 and \
                                v[3] >= vm[req[1]][0]//2 and \
                                v[2] >= vm[req[1]][1]//2 and \
                                v[4] >= vm[req[1]][1]//2:
                            host[req[2]] = [req[1], k]             # 存放主机的部署信息 host = {主机号：[虚拟机类型，服务器ID]}
                            servers[k].append(req[2])              # servers = {服务器ID：[主机...]}
                            Day_needs[i][0] -= vm[req[1]][0]
                            Day_needs[i][1] -= vm[req[1]][1]
                            v[1] -= vm[req[1]][0]//2           # 更新服务器池的信息
                            v[2] -= vm[req[1]][1]//2
                            v[3] -= vm[req[1]][0]//2
                            v[4] -= vm[req[1]][1]//2
                            flag = 1
                            NUM_VM += 1
                            break
                        else:
                            continue
                    else:                                       # 单节点部署
                        # 判断节点是否可以部署
                        if v[1] >= vm[req[1]][0] and v[2] >= vm[req[1]][1]:
                            if i < Days//6:           # 前一半
                                r = 1 if vm[req[1]][3] >= 1 else 0.3
                                if value_rd(vm[req[1]][3], round(v[1]/v[2], 1), r):
                                    host[req[2]] = [req[1], k, 'A']  # [虚拟机类型，服务器ID，节点]
                                    servers[k].append(req[2])
                                    v[1] -= vm[req[1]][0]  # 更新服务器池的信息
                                    v[2] -= vm[req[1]][1]
                                    Day_needs[i][0] -= vm[req[1]][0]
                                    Day_needs[i][1] -= vm[req[1]][1]
                                    flag = 1
                                    NUM_VM += 1
                                    break
                            else:
                                host[req[2]] = [req[1], k, 'A']  # [虚拟机类型，服务器ID，节点]
                                servers[k].append(req[2])
                                v[1] -= vm[req[1]][0]  # 更新服务器池的信息
                                v[2] -= vm[req[1]][1]
                                Day_needs[i][0] -= vm[req[1]][0]
                                Day_needs[i][1] -= vm[req[1]][1]
                                flag = 1
                                NUM_VM += 1
                                break
                        elif v[3] >= vm[req[1]][0] and v[4] >= vm[req[1]][1]:
                            if i < Days//6:
                                r = 1 if vm[req[1]][3] >= 1 else 0.3
                                if value_rd(vm[req[1]][3], round(v[3]/v[4], 1), r):
                                    host[req[2]] = [req[1], k, 'B']  # [虚拟机类型，服务器ID，节点]
                                    servers[k].append(req[2])
                                    v[3] -= vm[req[1]][0]  # 更新服务器池的信息
                                    v[4] -= vm[req[1]][1]
                                    Day_needs[i][0] -= vm[req[1]][0]
                                    Day_needs[i][1] -= vm[req[1]][1]
                                    flag = 1
                                    NUM_VM += 1
                                    break
                            else:
                                host[req[2]] = [req[1], k, 'B']  # [虚拟机类型，服务器ID，节点]
                                servers[k].append(req[2])
                                v[3] -= vm[req[1]][0]  # 更新服务器池的信息
                                v[4] -= vm[req[1]][1]
                                Day_needs[i][0] -= vm[req[1]][0]
                                Day_needs[i][1] -= vm[req[1]][1]
                                flag = 1
                                NUM_VM += 1
                                break
                        else:
                            continue
                if flag == 0:
                    # 部署失败，需要扩容服务器
                    # vm = {型号：[CPU，RAM，单双，crr]}
                    r = 0.2
                    while True:
                        flag1 = 0           # 标志是否扩容成功
                        for ser in serv:
                            crr = round(Day_needs[i][0] / Day_needs[i][1], 1)
                            if crr < 0.5:
                                crr = 0.5
                            elif crr > 3:
                                crr = 3
                            if value_rd(crr, ser[5], r) and \
                                    ser[1] // 2 >= vm[req[1]][0] and \
                                    ser[2] // 2 >= vm[req[1]][1]:
                                # 购买服务器
                                serv_poll[NUM] = [ser[0], ser[1] // 2, ser[2] // 2, ser[1] // 2, ser[2] // 2]
                                day_serv.append([NUM, ser[0]])          # 服务器id, 服务器型号
                                if ser[0] in day_serv_kind:
                                    day_serv_kind[ser[0]] += 1
                                else:
                                    day_serv_kind[ser[0]] = 1
                                flag1 = 1
                                # 部署虚拟机
                                if vm[req[1]][2] == 1:
                                    host[req[2]] = [req[1], NUM]  # 存放主机的部署信息 host = {主机号：[虚拟机类型，服务器ID]}
                                    servers[NUM] = [req[2]]
                                    serv_poll[NUM][1] -= vm[req[1]][0] // 2  # 更新服务器池的信息
                                    serv_poll[NUM][2] -= vm[req[1]][1] // 2
                                    serv_poll[NUM][3] -= vm[req[1]][0] // 2
                                    serv_poll[NUM][4] -= vm[req[1]][1] // 2
                                    Day_needs[i][0] -= vm[req[1]][0]
                                    Day_needs[i][1] -= vm[req[1]][1]
                                    NUM_VM += 1
                                else:
                                    host[req[2]] = [req[1], NUM, 'A']  # [虚拟机类型，服务器ID，节点]
                                    servers[NUM] = [req[2]]
                                    serv_poll[NUM][1] -= vm[req[1]][0]  # 更新服务器池的信息
                                    serv_poll[NUM][2] -= vm[req[1]][1]
                                    Day_needs[i][0] -= vm[req[1]][0]
                                    Day_needs[i][1] -= vm[req[1]][1]
                                    NUM_VM += 1
                                NUM += 1
                                break
                        if flag1 == 1:
                            break
                        else:
                            if vm[req[1]][3] > 1:
                                r += 1
                            else:
                                r += 0.1

            else:
                # 请求为 del
                # serv_poll[NUM] = [ser[0], ser[1] / 2, ser[2] / 2, ser[1] / 2, ser[2] / 2]
                if vm[host[req[1]][0]][2] == 1:                # 要删除的主机是双节点部署
                    serv_poll[host[req[1]][1]][1] += vm[host[req[1]][0]][0]//2
                    serv_poll[host[req[1]][1]][3] += vm[host[req[1]][0]][0]//2
                    serv_poll[host[req[1]][1]][2] += vm[host[req[1]][0]][1]//2
                    serv_poll[host[req[1]][1]][4] += vm[host[req[1]][0]][1]//2
                else:
                    # host[req[2]] = [req[1], k, 'A']
                    if host[req[1]][2] == 'A':
                        serv_poll[host[req[1]][1]][1] += vm[host[req[1]][0]][0]
                        serv_poll[host[req[1]][1]][2] += vm[host[req[1]][0]][1]
                    else:
                        serv_poll[host[req[1]][1]][3] += vm[host[req[1]][0]][0]
                        serv_poll[host[req[1]][1]][4] += vm[host[req[1]][0]][1]

        # 修改服务器ID
        # day_serv = [服务器id, 服务器型号]
        # day_serv_kind = {服务器型号：数量}
        # host = {主机号：[虚拟机类型，服务器ID]}
        # serv_poll[NUM] = [ser[0], ser[1] / 2, ser[2] / 2, ser[1] / 2, ser[2] / 2]
        # servers = {服务器ID：[主机...]}
        pre_serv_poll = {}
        if len(day_serv_kind) != len(day_serv):
            star = NUM - len(day_serv)
            for num in range(star, NUM):                # 记录修改之前的资源池信息
                 pre_serv_poll[num] = serv_poll[num]
            for key in day_serv_kind.keys():
                for j in range(day_serv_kind[key]):
                    for k, v in pre_serv_poll.items():
                        if v[0] == key:
                            serv_poll[star] = v
                            for temp in servers[k]:
                                host[temp][1] = star
                            pre_serv_poll.pop(k)
                            star += 1
                            break

        # 输出购买信息
        print("(purchase, %s)" % len(day_serv_kind))
        for k, v in day_serv_kind.items():
            print("(%s, %s)" % (k, v))

        # 输出迁移信息
        # day_move = {主机：[目的服务器, ]}
        nums_of_move = len(day_move)
        print("(migration, %s)" % nums_of_move)
        for h, s in day_move.items():
            if len(s) == 1:
                print("(%s, %s)" % (h, s[0]))
            else:
                print("(%s, %s, %s)" % (h, s[0], s[1]))
        for req in Reqs[i]:
            if req[0] == 'add':
                if vm[req[1]][2] == 1:
                    print("(%s)" % host[req[2]][1])
                else:
                    print("(%s, %s)" % (host[req[2]][1], host[req[2]][2]))


if __name__ == "__main__":
    main()

