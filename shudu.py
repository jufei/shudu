#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
c_shudu 定义了数独对象
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

subtext = '''
X X 7   X X X   5 X X
X X X   X X X   9 8 1
X X X   X X 1   X 7 4

7 6 X   X X 8   X X X
X 4 5   9 X 7   3 X X
X 8 X   X 4 5   X X X

X 1 3   7 8 X   X 5 X
X X X   X X X   1 X X
X X X   X X X   X 9 3

'''

from gong import c_gong
from cell import c_cell
from cell import yl
import copy


class c_shudu(object):

    def __init__(self, text):
        self.text = text
        self.cells = []
        self.gongs = []
        self.demision = 8

        if 'X' in text:
            self.parse_local(text)
        elif '*' in text:
            self.parse_lines()
        elif 'http' in text:
            self.parse_logdata(self.get_timu(text))
        else:
            self.parse_logdata(text)

    def parse_local(self, text):
        lines = [x.strip() for x in text.splitlines() if x.strip()]
        lines = [line.replace('X', '*').replace(' ', '') for line in lines]
        self.parse_lines(lines)

    def parse_file(self, filename):
        #  *****79**
        lines = open(filename).readlines()
        lines = [x.strip() for x in lines if x.strip()]
        self.parse_lines()

    def parse_logdata(self, logdata):
        lines = []
        for i in range(10):
            data = logdata[i * 9: i * 9 + 9]
            if data.strip():
                line = ''
                for number in data:
                    if int(number) == 0:
                        line += '*'
                    else:
                        line += number
                lines.append(line)
        self.parse_lines(lines)

    def parse_lines(self, lines):
        py = 9
        for line in lines:
            px = 1
            for number in line:
                cell = c_cell(px, py, number)
                cell.selfcheck()
                px += 1
                self.cells.append(cell)
            py = py - 1

    def get_timu(self, url):
        import requests
        headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
        rn = requests.get(url, headers=headers, proxies={'http': 'http://10.144.1.10:8080'})
        lines = rn.content.splitlines()
        lines = [str(x).split('=')[-1] for x in lines if 'tmda=' in str(x)][0]
        return lines.replace(';', '').replace("'", '').replace("'", '')[:81]

    def getcell(self, x, y):
        return [cell for cell in self.cells if cell.x == x and cell.y == y][0]

    def display(self):
        print('\n           1   2    3    4    5    6    7    8     9')
        for py in range(9, 0, -1):
            print('        +----+----+----+----+----+----+----+----+----+')
            row = '  {}     '.format(yl[py - 1])
            for px in range(1, 10):
                value = self.getcell(px, py).value
                value = value if value != -1 else ' '
                row += '|  {} '.format(value)
            row += '|    {}'.format(yl[py - 1])
            print(row)
        print('        +----+----+----+----+----+----+----+----+----+')
        print('           1   2    3    4    5    6    7    8     9\n')

    def arrange_gong(self):
        #  初始化所有的行宫
        for py in range(9, 0, -1):
            self.gongs.append(c_gong([cell for cell in self.cells if cell.y == py]))

        #  初始化所有的列宫
        for px in range(1, 10):
            self.gongs.append(c_gong([cell for cell in self.cells if cell.x == px]))

        # 初始化所有的3格宫
        for cy in [8, 5, 2]:
            for cx in [2, 5, 8]:
                cells = []
                for px in [cx - 1, cx, cx + 1]:
                    for py in [cy - 1, cy, cy + 1]:
                        cells.append(self.getcell(px, py))
                self.gongs.append(c_gong(cells, (cx, cy)))

    def get_snap_shot(self):
        snap = []
        for cell in self.cells:
            snap.append('{}  {}  {}  {}  '.format(cell.x, cell.y, cell.value, cell.cand_list))
        return snap

    def think(self):
        resolved = []
        round_count = 1
        result = True
        snap = self.get_snap_shot()
        while True:
            print('第 {} 轮：'.format(round_count))
            round_count += 1
            for gong in self.gongs:
                gong.think()

            if not self.health_check():
                self.display()
                print('数独全面检查失败！！！')
                break
            self.display()
            # if self.done():
            #     print('计算成功！')
            #     break
            new_snap = self.get_snap_shot()
            if new_snap == snap:
                break
            else:
                snap = new_snap

    def health_check(self):
        for gong in self.gongs:
            if not gong.health_check():
                print('gong is not health: {}'.format(gong))
                return False
        return True

    def done(self):
        return sum([cell.value for cell in self.cells if cell.cand_list == []]) == 45 * 9

    def inside_display(self):
        for py in range(9, 0, -1):
            print('+----+----+----+----+----+----+----+----+----+')
            row = ''
            for px in range(1, 10):
                value = str(self.getcell(px, py).cand_list)
                row += '| {}  '.format(value)
            row += '|'
            print(row)
        print('+----+----+----+----+----+----+----+----+----+')

    def arrange_gong_group(self):
        gongs = [gong for gong in self.gongs if gong.type == 'cell_gong']

        for ty in [9, 6, 3]:
            self.gong_groups.append(c_gong_group(
                [gong for gong in gongs if max([cell.y for cell in gong.cells]) == ty]))

        for tx in [3, 6, 9]:
            self.gong_groups.append(c_gong_group(
                [gong for gong in gongs if max([cell.x for cell in gong.cells]) == tx]))

    def get_yanjin_cells(self):
        two_cand_cells = [cell for cell in self.cells if len(cell.cand_list) == 2]
        cands = {}
        for cell in two_cand_cells:
            label = ' '.join([str(x) for x in cell.cand_list])
            if label in cands:
                cands[label].append(cell)
            else:
                cands[label] = [cell]

                demision = self.demision
        result = []
        keys = list(cands.keys()) * self.demision
        while demision > 0:
            for cand in cands:
                if cands[cand]:
                    result.append(cands[cand][0])
                    del(cands[cand][0])
                    demision -= 1
                    if demision == 0:
                        break
        print('可用的演进Cell数为：{}'.format(len(two_cand_cells)))
        return result

    def get_all_path(self):
        cell_list = self.get_yanjin_cells()
        path_list = []
        for cell in cell_list:
            if path_list:
                new_list = []
                for path in path_list:
                    new_list.append(path + [(cell.x, cell.y, cell.cand_list[0])])
                    new_list.append(path + [(cell.x, cell.y, cell.cand_list[1])])
                path_list = new_list
            else:
                path_list = [[(cell.x, cell.y, cell.cand_list[0])],
                             [(cell.x, cell.y, cell.cand_list[1])]]
        return path_list

    def apply_path(self, path):
        for node in path:
            x, y, v = node
            self.getcell(x, y).assert_value(v)

    def yanjin(self):
        path_list = self.get_all_path()
        count = 1
        for path in path_list:
            print('尝试路径：{} {}'.format(count, path))
            tmpshudu = copy.deepcopy(self)
            tmpshudu.apply_path(path)
            tmpshudu.think()
            if tmpshudu.health_check():
                if tmpshudu.done():
                    print('尝试路径 {} 成功！'.format(count))
                    return 0
                else:
                    print('尝试路径 {} 失败，继续。'.format(count))
            else:
                print('尝试路径 {} 失败，继续。'.format(count))
            count += 1

    def resolve(self):
        self.arrange_gong()
        self.think()
        if self.done():
            print('搞定！')
            self.display()
        else:
            self.yanjin()


if __name__ == '__main__':
    subtext = 'http://www.cn.sudokupuzzle.org/printable.php?nd=4&y=2018&m=07&d=13'
    shudu = c_shudu(subtext)
    shudu.demision = 9
    shudu.resolve()
