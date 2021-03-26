# -*- coding:utf-8 -*-
"""
日期：2021年03月12日
"""

import time
import sys
serv = []           # 服务器
serv_dict = {}
vm = {}             # 虚拟机
Reqs = []            # 请求
Days = 0
Arg1 = 0.67
Arg2 = 0.33
Day_needs = []       # 每一天的CPU和RAM需求

yanzheng = {}
cost = 0
yan_n = 0


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
        crr = round(line[1] / line[2], 1)
        line.append(crr)
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
    # to read standard input
    # process
    # to write standard output
    # sys.stdout.flush()
    global cost
    global yan_n
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
        move_num = NUM_VM // 200                        # 迁移数量不能超过当前VM的5/1000
        if NUM and move_num:
            num_of_ser = NUM - 1
            while move_num > 0:
                for h in servers[num_of_ser]:           # servers = {服务器ID：[主机...]}
                    for k, v in serv_poll.items():      # serv_poll = {服务器ID：[型号，两个节点的资源]}
                        if k >= num_of_ser:
                            break
                        if vm[host[h][0]][2] == 1:
                            if v[1] >= vm[host[h][0]][0]//2 and \
                                    v[3] >= vm[host[h][0]][0]//2 and \
                                    v[2] >= vm[host[h][0]][1]//2 and \
                                    v[4] >= vm[host[h][0]][1]//2:
                                day_move[h] = [num_of_ser, k]
                                v[1] -= vm[host[h][0]][0] // 2  # 更新服务器池的信息
                                v[2] -= vm[host[h][0]][1] // 2
                                v[3] -= vm[host[h][0]][0] // 2
                                v[4] -= vm[host[h][0]][1] // 2
                                serv_poll[num_of_ser][1] += vm[host[h][0]][0] // 2
                                serv_poll[num_of_ser][2] += vm[host[h][0]][1] // 2
                                serv_poll[num_of_ser][3] += vm[host[h][0]][0] // 2
                                serv_poll[num_of_ser][4] += vm[host[h][0]][1] // 2
                                servers[num_of_ser].remove(h)
                                servers[k].append(h)
                                host[h][1] = k
                                move_num -= 1
                                break
                        else:
                            if v[1] >= vm[host[h][0]][0] and v[2] >= vm[host[h][0]][1]:
                                # day_move[h] = [k, 'A']
                                servers[num_of_ser].remove(h)
                                servers[k].append(h)
                                v[1] -= vm[host[h][0]][0]   # 更新服务器池的信息
                                v[2] -= vm[host[h][0]][1]
                                if host[h][2] == 'A':
                                    day_move[h] = [num_of_ser, 'A', k, 'A']
                                    serv_poll[num_of_ser][1] += vm[host[h][0]][0]
                                    serv_poll[num_of_ser][2] += vm[host[h][0]][1]
                                else:
                                    day_move[h] = [num_of_ser, 'B', k, 'A']
                                    serv_poll[num_of_ser][3] += vm[host[h][0]][0]
                                    serv_poll[num_of_ser][4] += vm[host[h][0]][1]
                                move_num -= 1
                                host[h][1] = k
                                host[h][2] = 'A'
                                break
                            elif v[3] >= vm[host[h][0]][0] and v[4] >= vm[host[h][0]][1]:
                                # day_move[h] = [k, 'B']
                                servers[num_of_ser].remove(h)
                                servers[k].append(h)
                                v[3] -= vm[host[h][0]][0]   # 更新服务器池的信息
                                v[4] -= vm[host[h][0]][1]
                                if host[h][2] == 'A':
                                    day_move[h] = [num_of_ser, 'A', k, 'B']
                                    serv_poll[num_of_ser][1] += vm[host[h][0]][0]
                                    serv_poll[num_of_ser][2] += vm[host[h][0]][1]
                                else:
                                    day_move[h] = [num_of_ser, 'B', k, 'B']
                                    serv_poll[num_of_ser][3] += vm[host[h][0]][0]
                                    serv_poll[num_of_ser][4] += vm[host[h][0]][1]
                                move_num -= 1
                                host[h][1] = k
                                host[h][2] = 'B'
                                break
                    if move_num == 0:
                        break
                if len(servers[num_of_ser]) == 0:       # 当前服务器迁移完
                    num_of_ser -= 1
                else:
                    break

        # 处理当天请求
        

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
                servers[host[req[1]][1]].remove(req[1])

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
            change_serv = {}
            for key in day_serv_kind.keys():
                for j in range(day_serv_kind[key]):
                    for k, v in pre_serv_poll.items():
                        if v[0] == key:
                            serv_poll[star] = v
                            for temp in servers[k]:
                                host[temp][1] = star
                            change_serv[star] = servers[k]
                            pre_serv_poll.pop(k)
                            star += 1
                            break
            servers.update(change_serv)

        # 输出购买信息
        # print("(purchase, %s)" % len(day_serv_kind))
        # for k, v in day_serv_kind.items():              # {型号：数量}
        #     print("(%s, %s)" % (k, v))
        #
        # # 输出迁移信息
        # # day_move = {主机：[目的服务器, ]}
        # nums_of_move = len(day_move)
        # print("(migration, %s)" % nums_of_move)
        # for h, s in day_move.items():           # day_move = {主机ID：[目的服务器] }
        #     if len(s) == 1:
        #         print("(%s, %s)" % (h, s[0]))
        #     else:
        #         print("(%s, %s, %s)" % (h, s[0], s[1]))
        # for req in Reqs[i]:
        #     if req[0] == 'add':
        #         if vm[req[1]][2] == 1:
        #             print("(%s)" % host[req[2]][1])
        #         else:
        #             print("(%s, %s)" % (host[req[2]][1], host[req[2]][2]))



        for k, v in day_serv_kind.items():              # {型号：数量}
            print("(%s, %s)" % (k, v))
            for n in range(v):
                yanzheng[yan_n] = [serv_dict[k][0]//2, serv_dict[k][1]//2, serv_dict[k][0]//2, serv_dict[k][1]//2]
                yan_n += 1
            cost += serv_dict[k][2] * v

        # 输出迁移信息
        # day_move = {主机：[目的服务器, ]}
        nums_of_move = len(day_move)
        # print("(migration, %s)" % nums_of_move)
        for h, s in day_move.items():           # day_move = {主机ID：[原服务器，目的服务器] }
            if len(s) == 2:
                yanzheng[s[0]][0] += vm[host[h][0]][0] // 2
                if yanzheng[s[0]][0] > serv_dict[s[0]][0]//2:
                    print("资源超出限制：")
                    print(h, s)
                yanzheng[s[0]][1] += vm[host[h][0]][1] // 2
                if yanzheng[s[0]][1] > serv_dict[s[0]][1]//2:
                    print("资源超出限制：")
                    print(h, s)
                yanzheng[s[0]][2] += vm[host[h][0]][0] // 2
                if yanzheng[s[0]][2] > serv_dict[s[0]][0]//2:
                    print("资源超出限制：")
                    print(h, s)
                yanzheng[s[0]][3] += vm[host[h][0]][1] // 2
                if yanzheng[s[0]][3] > serv_dict[s[0]][1]//2:
                    print("资源超出限制：")
                    print(h, s)

                yanzheng[s[1]][0] -= c // 2
                if yanzheng[s[1]][0] < 0:
                    print("迁移出错：资源超出限制")
                    print(h, s)
                yanzheng[s[1]][1] -= vm[host[h][0]][1] // 2
                if yanzheng[s[1]][1] < 0:
                    print("迁移出错：资源超出限制")
                    print(h, s)
                yanzheng[s[1]][2] -= vm[host[h][0]][0] // 2
                if yanzheng[s[1]][2] < 0:
                    print("迁移出错：资源超出限制")
                    print(h, s)
                yanzheng[s[1]][3] -= vm[host[h][0]][1] // 2
                if yanzheng[s[1]][3] < 0:
                    print("迁移出错：资源超出限制")
                    print(h, s)

            else:
                if s[1] == 'A':              # 原来在A节点
                    yanzheng[s[0]][0] += vm[host[h][0]][0]              # cpu
                    if yanzheng[s[0]][0] > serv_dict[s[0]][0] // 2:
                        print("资源超出限制：")
                        print(h, s)
                    yanzheng[s[0]][1] += vm[host[h][0]][1]              # ram
                    if yanzheng[s[0]][1] > serv_dict[s[0]][1] // 2:
                        print("资源超出限制：")
                        print(h, s)

        for req in Reqs[i]:
            if req[0] == 'add':
                if vm[req[1]][2] == 1:
                    print("(%s)" % host[req[2]][1])
                else:
                    print("(%s, %s)" % (host[req[2]][1], host[req[2]][2]))

        # print(serv_poll)
        # print("********************")


if __name__ == "__main__":
    # start = time.time()
    main()
    # end = time.time()
    # print("用时：%s" % (start-end))
