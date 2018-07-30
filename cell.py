#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
c_cell 定义了九宫格中的某个格子
坐标：x,y, 以九宫格左下角为圆点；
对每个格子有编号，纵坐标从上向下依次为ABCDEFGHI, 横坐标为123456789
所以，用A2这样的形式来表示某个格子

        +----+----+----+----+----+----+----+----+----+
  A     |    |    |    | 3  | 6  | 7  | 9  |    | 2  |
        +----+----+----+----+----+----+----+----+----+
  B     | 6  |    |    | 9  | 5  | 2  |    | 7  | 4  |
        +----+----+----+----+----+----+----+----+----+
  C     | 9  | 2  | 7  | 1  | 4  | 8  | 6  | 5  | 3  |
        +----+----+----+----+----+----+----+----+----+
  D     |    |    | 4  | 7  | 1  | 3  |    |    | 9  |
        +----+----+----+----+----+----+----+----+----+
  E     |    |    | 9  | 2  | 8  | 4  | 7  |    | 5  |
        +----+----+----+----+----+----+----+----+----+
  F     | 7  |    |    | 6  | 9  | 5  |    |    | 1  |
        +----+----+----+----+----+----+----+----+----+
  G     |    |    | 6  |    | 7  | 9  |    | 2  | 8  |
        +----+----+----+----+----+----+----+----+----+
  H     |    | 9  | 8  |    | 2  | 6  | 3  |    | 7  |
        +----+----+----+----+----+----+----+----+----+
  I     |    | 7  |    | 8  | 3  | 1  |    | 9  | 6  |
        +----+----+----+----+----+----+----+----+----+

           1   2    3    4    5    6    7    8     9



'''

yl = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
yl = sorted(yl, reverse=True)


class c_cell(object):

    def __init__(self, x, y, input):
        self.x = x
        self.y = y
        if str(input).isdigit():
            self.value = int(input)
            self.cand_list = []
        else:
            self.value = -1
            self.cand_list = [x for x in range(1, 10)]
        self.name = '格子{}{}'.format(yl[self.y - 1], self.x)

    def _name(self):
        return '格子{}{}'.format(yl[self.y - 1], self.x)

    def detail(self):
        if self.cand_list:
            return '{},可选值：{}'.format(self._name(), self.cand_list)
        else:
            return '{},值：{}'.format(self._name().x, self.value)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def selfcheck(self):
        if len(self.cand_list) == 1:
            print('格子 {}-{} 只有1个可选值，确定为{}'.format(self.x, self.y, self.cand_list[0]))
            self.value = int(self.cand_list[0])
            self.cand_list = []
            return True
        else:
            return False

    def remove_cand(self, cand):
        if cand in self.cand_list:
            self.cand_list.remove(int(cand))
            print('{}的候选项中移除{}, 剩余：{}'.format(self._name(), cand, self.cand_list))

    def showv(self):
        return self.value if self.value != -1 else ''

    def status(self):
        return self.value != -1

    def assert_value(self, value):
        print('确定 {} 的值为：{}'.format(self, value))
        self.value = int(value)
        self.cand_list = []
