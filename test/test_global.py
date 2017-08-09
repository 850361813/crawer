# -*- coding: utf-8 -*-

init_fetch_num = 0


def add_glob():
    global init_fetch_num
    init_fetch_num = init_fetch_num + 1
    print init_fetch_num


if __name__ == '__main__':
    add_glob()
    add_glob()
    add_glob()