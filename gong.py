#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
c_gong 定义了九宫格中的某个格子

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

宫有3种：
    1、行宫，如 行宫A，行宫B
    2、列宫，如 列宫1，列宫2
    3、9格宫，这里我们给每个9格宫一个编号，从上向下，从左往右，依次是1-9

所以 一个九宫格有18个宫


'''


from cell import yl, c_cell


class c_gong(object):

    def __init__(self, celllist=[], key=None):
        self.cells = celllist
        if len(set([cell.x for cell in self.cells])) == 1:
            self.type = 'col_gong'
            self.index = self.cells[0].x
            self.name = '列宫{}'.format(self.index)
        elif len(set([cell.y for cell in self.cells])) == 1:
            self.type = 'line_gong'
            self.index = self.cells[0].y
            self.name = '行宫{}'.format(yl[self.index - 1])
        else:
            self.type = 'cell_gong'
            self.cx, self.cy = key
            gong_map = ['B2', 'B5', 'B8', 'E2', 'E5', 'E8', 'H2', 'H5', 'H8']
            self.center = '{}{}'.format(yl[self.cy - 1], self.cx)
            self.index = gong_map.index(self.center) + 1
            self.name = '九格宫{}'.format(self.index)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def selfcheck(self):
        # print('{}的自我检查: '.format(self))
        result = True
        for cell in self.cells:
            for v in self._know_values():
                cell.remove_cand(v)

        count = 0
        for cell in self.cells:
            if cell.selfcheck():
                print('格子{}-{} 只有{}了。'.format(cell.x, cell.y, cell.value))
                count += 1
        return count > 0

    def _know_values(self):
        return [cell.value for cell in self.cells if cell.value != -1]

    def _other_cells(self, cell):
        return [acell for acell in self.cells if acell.x != cell.x or acell.y != cell.y]

    def _get_subset(self, alist):
        r = []
        for i in range(len(alist)):
            for j in range(len(alist)):
                for k in range(len(alist)):
                    p = [alist[i], alist[j], alist[k]]
                    p = sorted(p)
                    if len(set(p)) == 3:
                        if p not in r:
                            r.append(p)
        return r

    def think0(self):
        resoulved_cell = []
        # 方法1： 对一宫内，看看哪些值已经出现了，然后把已经出现的值，从cell的候选列表中去除
        if self.selfcheck():
            return True

        # 方法2： 对一宫内，如果某个格子的可选值里面，有个值其他格子都没有，那么这个格子就是这个值
        for cell in self.cells:
            other_all_cands = []
            other_cells = [ocell for ocell in self.cells if ocell.x != cell.x or
                           ocell.y != cell.y]
            for ocell in other_cells:
                other_all_cands += ocell.cand_list
            other_all_cands = list(set(other_all_cands))
            unique_value = [v for v in cell.cand_list if v not in other_all_cands]
            if len(unique_value) == 1:
                print('发现格子:{}-{}的可选值 {} 其他格子都没有, 所以格子 {}-{} 就是{}。'.format(
                    cell.x, cell.y, unique_value[0], cell.x, cell.y, unique_value[0]))
                cell.assert_value(unique_value[0])
                return True

        # 方法3： 如果有2个格子有相同的2个待选值，那么，其他格子的待选值就必然没有这2个值；
        #      例如：如果有2个格子，待选值都是3,8； 那么，3 8 就只能在这2个格子里面，其他的格子就
        #            不可能是3或8，所以就可以把3和8从其他的格子的待选列表中去除

        two_cand_cells = [x for x in self.cells if len(x.cand_list) == 2]
        for cell in two_cand_cells:
            other_cells = self._other_cells(cell)
            same_cand_cells = [acell for acell in other_cells if
                               acell.cand_list == cell.cand_list]
            if same_cand_cells:  # 确认有另外一个格子，和当前格子一样，是相同的2个候选值
                print('方法3发现了：宫：{}，格子：{}-{}, 相同格子：{}-{}, 相同候选值：{}'.format(
                    self, cell.x, cell.y, same_cand_cells[0].x, same_cand_cells[0].y,
                    cell.cand_list))
                found = False
                for dcell in [x for x in other_cells if x.cand_list != cell.cand_list]:
                    for v in cell.cand_list:
                        dcell.remove_cand(v)
                        found = found or dcell.selfcheck()
                return found
                # return True

        # 方法4：如果有3个格子，他们的可选值是3个值，并且这3个格子的可选值相同，那么其他格子的可选
        # 值就不能是这3个可选值； 这个是方法3拓展到3个格子的时候的情况；

        three_cand_cells = [x for x in self.cells if len(x.cand_list) == 3]
        for cell in three_cand_cells:
            other_cells = self._other_cells(cell)
            same_cand_cells = [acell for acell in other_cells if
                               acell.cand_list == cell.cand_list]
            if len(same_cand_cells) == 2:  # 确认有另外两个格子，和当前格子一样，是相同的3个候选值
                print(('方法4发现了：宫：{}，格子：{}-{}, 相同格子：{}-{} 和 {}-{}, '
                       '相同候选值：{}').format(
                    self, cell.x, cell.y,
                    same_cand_cells[0].x, same_cand_cells[0].y,
                    same_cand_cells[1].x, same_cand_cells[1].y,
                    cell.cand_list))
                for dcell in [x for x in other_cells if x.cand_list != cell.cand_list]:
                    for v in cell.cand_list:
                        dcell.remove_cand(v)
                        if dcell.selfcheck():
                            return True

        # 方法5： 三链数删减法：一宫内，有3个格子，每个格子的候选数是2个，但是3个格子的候选数成链，
        #          如：(1,2), (1,3), (2, 3) 那么，其他格子就不能有123作为候选数
        #         另外，这个可以扩充，比如：(1,2), (1,3), (1,2,3) 也是满足三链数的
        # 同样的规则，可以形成四链数，比如：(12,23,34,14) 就是四链数，(123,123,14,1234)也是四链数

        # 找出所有候选值少于等于3个的格子，要求这些格子数必须大于或等于3
        print(str(self))
        three_cand_cells = [x for x in self.cells if x.cand_list and len(x.cand_list) <= 3]
        left_cells = [x for x in self.cells if x.cand_list]
        print('**************', len(three_cand_cells), len(left_cells))
        if len(three_cand_cells) >= 3 and len(left_cells) > 3:
            print('{} ********************************************'.format(self))
            # 找出这些格子的候选值构成的，可能的三链，比如：12,23,13，那么三链就是123
            values = []
            for cell in three_cand_cells:
                values += cell.cand_list
            values = list(set(values))  # 所有可能的值
            # Values就是所有可能的值，我们用这些值来组三链
            print(values)

            setgroup = self._get_subset(values)
            print(len(setgroup))

            #  setgroup是所有可能的组合，比如(1,2,3)
            for group in setgroup:  # 对任意一个组合，看有多少个子集，如果子集数刚好是3，就形成链
                chains_cells = [acell for acell in three_cand_cells if
                                set(acell.cand_list).issubset(set(group))]
                if len(chains_cells) == 3:
                    print('方法5发现了三链数，链:{}'.format(group))
                    for cell in self.cells:
                        print(cell)
                    chain_tags = ['{}{}'.format(acell.x, acell.y) for acell in chains_cells]
                    other_cells = [acell for acell in self.cells if
                                   '{}{}'.format(acell.x, acell.y) not in chain_tags]
                    for v in group:
                        for ocell in other_cells:
                            ocell.remove_cand(v)
                    return True

        return False

    def walk(self):
        total_resolved = []
        new_resolved_cells = self.think()
        total_resolved += new_resolved_cells
        return total_resolved

    def getcell(self, px, py):
        return [cell for cell in self.cells if cell.x == px and cell.y == py][0]

    def show(self):
        if self.type == 'line_gong':
            print('+----+----+----+----+----+----+----+----+----+')
            row = ''
            for px in range(1, 10):
                py = self.cells[0].y
                value = self.getcell(px, py).value
                value = value if value != -1 else ' '
                row += '| {}  '.format(value)
            row += '|'
            print(row)
            print('+----+----+----+----+----+----+----+----+----+')

        if self.type == 'col_gong':
            print('+----+')
            for py in range(9, 0, -1):
                px = self.cells[0].x
                value = self.getcell(px, py).value
                value = value if value != -1 else ' '
                print('| {}  |'.format(value))
                print('+----+')

    def health_check(self):
        values = [cell.value for cell in self.cells if cell.status()]
        kp_values = set(values)
        return len(kp_values) == len(values)

    def think(self):
        for i in range(20):
            funname = 'apply_rule_{}'.format(i + 1)
            if hasattr(self, funname):
                getattr(self, funname)()

    def apply_rule_1(self):
        print('对 [{}] 应用 [基础摒除法] ...'.format(self.name))
        for cell in self.cells:
            for v in self._know_values():
                cell.remove_cand(v)

    def apply_rule_2(self):
        print('对 [{}] 应用 [唯我有之法] ...'.format(self.name))

        # 方法2： 对一宫内，如果某个格子的可选值里面，有个值其他格子都没有，那么这个格子就是这个值
        for cell in self.cells:
            other_all_cands = []
            other_cells = [ocell for ocell in self.cells if ocell.x != cell.x or
                           ocell.y != cell.y]
            for ocell in other_cells:
                other_all_cands += ocell.cand_list
            other_all_cands = list(set(other_all_cands))
            unique_value = [v for v in cell.cand_list if v not in other_all_cands]
            if len(unique_value) == 1:
                print('[唯我有之法] 发现{}的可选值 {} 其他格子都没有, 所以格子{}就是{}。'.format(
                    cell, unique_value[0], cell.name, unique_value[0]))
                cell.assert_value(unique_value[0])

    def apply_rule_3(self):
        print('对 [{}] 应用 [两格相同2值法] ...'.format(self.name))
        # 方法3： 如果有2个格子有相同的2个待选值，那么，其他格子的待选值就必然没有这2个值；
        #      例如：如果有2个格子，待选值都是3,8； 那么，3 8 就只能在这2个格子里面，其他的格子就
        #            不可能是3或8，所以就可以把3和8从其他的格子的待选列表中去除

        two_cand_cells = [x for x in self.cells if len(x.cand_list) == 2]
        for cell in two_cand_cells:
            other_cells = self._other_cells(cell)
            same_cand_cells = [acell for acell in other_cells if
                               acell.cand_list == cell.cand_list]
            if same_cand_cells:  # 确认有另外一个格子，和当前格子一样，是相同的2个候选值
                print('[两格相同2值法] 发现了{}-{}, 相同格子：{}, 相同候选值：{}'.format(
                    self, cell, same_cand_cells[0], cell.cand_list))
                for dcell in [x for x in other_cells if x.cand_list != cell.cand_list]:
                    for v in cell.cand_list:
                        dcell.remove_cand(v)

    def apply_rule_4(self):
        print('对 [{}] 应用 [3格相同3值法] ...'.format(self.name))
        # 方法3： 如果有3个格子有相同的3个待选值，那么，其他格子的待选值就必然没有这3个值；

        three_cand_cells = [x for x in self.cells if len(x.cand_list) == 3]
        for cell in three_cand_cells:
            other_cells = self._other_cells(cell)
            same_cand_cells = [acell for acell in other_cells if
                               acell.cand_list == cell.cand_list]
            if len(same_cand_cells) == 2:  # 确认有另外两个格子，和当前格子一样，是相同的3个候选值
                print(('[3格相同3值法] 发现了 {}，格子：{}, 相同格子：{} 和 {}, '
                       '相同候选值：{}').format(
                    self, cell,
                    same_cand_cells[0],
                    same_cand_cells[1],
                    cell.cand_list))
                for dcell in [x for x in other_cells if x.cand_list != cell.cand_list]:
                    for v in cell.cand_list:
                        dcell.remove_cand(v)

    def apply_rule_5(self):
        print('对 [{}] 应用 [三链数删减法] ...'.format(self.name))
        # 方法5： 三链数删减法：一宫内，有3个格子，每个格子的候选数是2个，但是3个格子的候选数成链，
        #          如：(1,2), (1,3), (2, 3) 那么，其他格子就不能有123作为候选数
        #         另外，这个可以扩充，比如：(1,2), (1,3), (1,2,3) 也是满足三链数的
        # 同样的规则，可以形成四链数，比如：(12,23,34,14) 就是四链数，(123,123,14,1234)也是四链数

        # 找出所有候选值少于等于3个的格子，要求这些格子数必须大于或等于3
        three_cand_cells = [x for x in self.cells if x.cand_list and len(x.cand_list) <= 3]
        left_cells = [x for x in self.cells if x.cand_list]
        if len(three_cand_cells) >= 3 and len(left_cells) > 3:
            # 找出这些格子的候选值构成的，可能的三链，比如：12,23,13，那么三链就是123
            values = []
            for cell in three_cand_cells:
                values += cell.cand_list
            values = list(set(values))  # 所有可能的值
            # Values就是所有可能的值，我们用这些值来组三链

            setgroup = self._get_subset(values)

            #  setgroup是所有可能的组合，比如(1,2,3)
            for group in setgroup:  # 对任意一个组合，看有多少个子集，如果子集数刚好是3，就形成链
                chains_cells = [acell for acell in three_cand_cells if
                                set(acell.cand_list).issubset(set(group))]
                if len(chains_cells) == 3:
                    print('[三链数删减法] 发现了三链数，链:{}'.format(group))
                    for cell in self.cells:
                        print(cell)
                    chain_tags = ['{}{}'.format(acell.x, acell.y) for acell in chains_cells]
                    other_cells = [acell for acell in self.cells if
                                   '{}{}'.format(acell.x, acell.y) not in chain_tags]
                    for v in group:
                        for ocell in other_cells:
                            ocell.remove_cand(v)

    def apply_rule_6(self):
        print('对 [{}] 应用 [隐性三链数删减法] ...'.format(self.name))
        # 隐性三链删减法，是指如果有3个可选数，只出现在3个格子里面（不是3个格子都有），那么这3个数字
        # 只能存在于这3个格子；
        # 例如：5 只出现在格子A, B； 6只出现在A，7只出现在B，C； 那么567就只能出现在ABC里面，
        # 这个时候，就可以从其他格子的候选列表中删除567
        unknown_values = [x for x in range(1, 10) if x not in self._know_values()]
        if len(unknown_values) >= 4:
            p = {}
            for v in unknown_values:
                p[str(v)] = [cell for cell in self.cells if v in cell.cand_list]
            groups = self._get_subset(unknown_values)
            for group in groups:
                celllist = []
                for v in group:
                    celllist += [cell.name for cell in p[str(v)]]
                if len(list(set(celllist))) == 3:
                    other_values = []
                    for t in [x for x in self.cells if x.name not in celllist]:
                        other_values += t.cand_list
                    if set(other_values) & set(group):
                        print('[隐性三链数删减法] 发现了隐性链 {}'.format(group))
                        print(other_cells)
                        for cell in self.cells:
                            if cell.cand_list:
                                print(cell.detail())

                        for v in group:
                            for cell in [x for x in self.cells if x.cand_list and x.name not in
                                         [p for p in celllist]]:
                                cell.remove_cand(v)
