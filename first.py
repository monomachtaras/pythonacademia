file = open('/home/ubuntu/kali/text.txt', 'w')
list='abcdefghijklmnopqrstuvwxyz0123456789'
for x1 in list:
    for x2 in list:
        for x3 in list:
            for x4 in list:
                for x5 in list:
                    for x6 in list:
                        for x7 in list:
                            for x8 in list:
                                file.write(x1+x2+x3+x4+x5+x6+x7+x8)