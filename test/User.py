# -*- coding: utf-8 -*-

class User:

    name = None
    age = None

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def prt(self):
        print self.name + '--' + self.age

    def Run(self):
        pass

class Staff(User):
    def __init__(self, year):
        super
        self.year = year


class Work:

    def __init__(self, title, selary):
        self.title = title
        self.selary = selary

    def prt(self):
        print self.name + '--' + self.age

class Company:

    def __init__(self, user, work):
        self.user = user
        self.work = work
    def prt(self):
        print self.user.name
        print self.user.age
        print self.work.selary
        print self.work.title


if __name__ == '__main__':
        user = User(None, None)
        user.name = 'zhangsan'
        user.age = '28'
        user2 = User(None, None)
        user2.name = 'aaa'
        user2.age = '34'

        work = Work('职员', '1000')
        company = Company(user2, work)
        company.prt()

