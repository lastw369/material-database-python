# coding=utf-8
from pymatgen.io.ase import AseAtomsAdaptor
import re
from pymatgen.core.structure import Structure
from pymatgen.io.cif import CifWriter
from ase.io import read
from ase.visualize import view
from math import sin, cos, pi, sqrt
eps = 0.001


def num_multiple(lst, mult):
    lst_new = []
    for i in lst:
        lst_new.append(i * mult)
    return lst_new


def coords_transform(A1, B1, C1):
    A = A1 / 180 * pi
    B = B1 / 180 * pi
    C = C1 / 180 * pi
    z = sqrt(1 - cos(B) ** 2 - (cos(A)*sin(C))**2)
    a_vec = [1, 0, 0]
    b_vec = [cos(C), sin(C), 0]
    c_vec = [cos(B), cos(A) * sin(C), z]
    par_lst = [a_vec, b_vec, c_vec]

    for vec in par_lst:
        for i in range(3):
            if abs(vec[i]) < eps:
                vec[i] = 0
    return par_lst


class CIF:
    def __init__(self, crys):
        self.crys = crys
        f = AseAtomsAdaptor.get_structure(self.crys)
        f1 = str(f) + '\n'
        self.file = f1

    def to_cif(self):
        f = AseAtomsAdaptor.get_structure(self.crys)
        print(AseAtomsAdaptor.get_structure(self.crys))
        f1 = str(f) + '\n'
        self.file = f1
        # matrix
        # text = re.findall('abc\s\s\s:(.*?)\n', f1)
        # print(text)
        j_pv_lst = re.findall('abc(.*?)\n', f1)[0]  # abc   :  19.257300  19.569178  21.133988
        j1_pv_lst = j_pv_lst.split(' ')  # abc   :   6.419100   6.523059   7.044663
        # print(j1_pv_lst)
        while ':' in j1_pv_lst:
            j1_pv_lst.remove(':')
        while '' in j1_pv_lst:
            j1_pv_lst.remove('')
        # for num in j1_pv_lst:
        # print(float(num))
        a = float(j1_pv_lst[0])
        b = float(j1_pv_lst[1])
        c = float(j1_pv_lst[2])
        mutiple = [a, b, c]
        angles = re.findall('angles(.*?)\n', f1)[0]
        angles1 = angles.split(' ')
        while ':' in angles1:
            angles1.remove(':')
        while '' in angles1:
            angles1.remove('')
        angle_lst = []
        for i in angles1:
            num = float(i)
            angle_lst.append(num)
        # print(angle_lst)
        # print(mutiple)
        coords_lst1 = coords_transform(angle_lst[0], angle_lst[1], angle_lst[2])
        par_lst_matrix1 = [coords_lst1[0], coords_lst1[1], coords_lst1[2]]
        pri_vectors = []
        for i in range(len(par_lst_matrix1)):
            pri_vectors.append(num_multiple(par_lst_matrix1[i], mutiple[i]))
        par_lst_matrix = [pri_vectors[0],
                          pri_vectors[1],
                          pri_vectors[2]]
        # print(par_lst_matrix)


        # 物质种类（比如：Lu2 Al4）
        y1 = re.findall('Full\sFormula\s(.*?)\n', f1)[0]
        y1_lst = y1.lstrip('(').rstrip(')')
        material = re.findall('Full\sFormula\s(.*?)\n', f1)[0].lstrip('(').rstrip(')')
        self.mat_name = material
        elements = material.split(' ')
        #print(elements)              # (Re4 S8)\(Re108 S216)
        zmb_lst = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]
        szb_lst = [str(i) for i in range(0, 10)]
        element_lst = []
        number_lst =[]
        c = []
        for element in elements:       # 这个循环之后，得到原子与对应的原子数两个列表
            letter_lst = list(element)
            symbol_lst = []
            num_lst = []
            element_lst1 =[]
            number_lst1 =[]
            # print(letter_lst)
            for i in range(len(letter_lst)):
                if letter_lst[i] in szb_lst:
                    num_lst.append(letter_lst[i])
                    # print(num_lst)
                if letter_lst[i] in zmb_lst:
                    symbol_lst.append(letter_lst[i])
                    # print(symbol_lst)
                # print(num_lst)    # ['1', '0', '8', '2', '1', '6']
                # print(symbol_lst) # ['R', 'e', 'S']
                element1 = ''.join(symbol_lst)
                # print(element1)
                element_lst1.append(element1)
                #print(num_lst)
                number1 = ''.join(num_lst)
                number_lst1.append(number1)
                #print(number_lst1)
            ys = 'a'     # 元素
            gs = '0'     # 个数
            # print(element_lst1)
            for i in element_lst1:
                if len(i) >= len(ys):
                    ys = i
            element_lst.append(i)
            for i in number_lst1:
                if len(i) >= len(gs):
                    gs = i
            number_lst.append(i)
        #print(element_lst)
        #print(number_lst)

        par_lst_species = []                   # 用于Cifwrite参数(species)的
        for i in range(len(element_lst)):
            num = int(number_lst[i])
            for j in range(num):
                par_lst_species.append(element_lst[i])
        #print(par_lst_species)



        # 每个原子的坐标
        ord_lst = []   # 最终Cifwriter所需要的coords参数
        ord_lst1 = []
        ord_lst2 = []  # 储存的形式为
        for element in element_lst:
            ord_lst1 = re.findall(element+'\s\s\s\s(.*?)\n',f1)
            for ord in ord_lst1:
                ord1 = ord.split(' ')
                while '' in ord1:
                    ord1.remove('')
                ord_lst2.append(ord1)
        for ord in ord_lst2:
            ord1 = []
            for string in ord:
                num = float(string)
                ord1.append(num)
                if len(ord1) == 3:
                    ord2 = ord1
            ord_lst.append(ord2)
        par_lst_coords = ord_lst
        # print(par_lst_coords)

        # 构建Structure类
        structure = Structure(par_lst_matrix, par_lst_species, par_lst_coords)
        slab = CifWriter(structure, write_magmoms=True)   # struct (Structure) – structure to write; symprec (float) – If not none, finds the symmetry of the structure and writes the cif with symmetry information. Passes symprec to the SpacegroupAnalyzer; write_magmoms (bool) – If True, will write magCIF file. Incompatible with symprec
        slab.write_file('/Users/mac/Desktop/{}.cif'.format(self.mat_name))
        f = read('/Users/mac/Desktop/{}.cif'.format(self.mat_name))
        view(f)
        return '/Users/mac/Desktop/{}.cif'.format(self.mat_name)


# 在CIF的括号里输入一个Atoms，然后把路径改一下就能用了
if __name__ == '__main__':
    slab = read('/Users/mac/Desktop/2.cif')     # 随便找一个atoms对象用于生成cif文件
    CIF(slab).to_cif()
    print(slab.get_cell())
