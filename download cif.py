from pymatgen.ext.matproj import MPRester
import re
from pymatgen.core.structure import Structure
from pymatgen.io.cif import CifWriter
from ase.io import read
from ase.visualize import view
from Functions import coords_transform, num_multiple




class CIF:
    def __init__(self, mat_id):
        self.id = 'mp-'+str(mat_id)
    def to_cif(self):
        m = MPRester("pc0rARlba5Ae3SArM09")
        structure = m.query(self.id, ['initial_structure'])  # 改变不同的晶体ID录入不同的数字
        f = structure[0]['initial_structure']
        f1 = str(f) + '\n'
        print(f1)
        j_pv_lst = re.findall('abc(.*?)\n', f1)[0]   # abc   :  19.257300  19.569178  21.133988
        j1_pv_lst = j_pv_lst.split(' ')                     # abc   :   6.419100   6.523059   7.044663
        while ':' in j1_pv_lst:
            j1_pv_lst.remove(':')
        while '' in j1_pv_lst:
            j1_pv_lst.remove('')
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
        #print(mutiple)
        coords_lst1 = coords_transform(angle_lst[0], angle_lst[1], angle_lst[2])
        par_lst_matrix1 = [coords_lst1[0],coords_lst1[1],coords_lst1[2]]
        pri_vectors = []
        for i in range(len(par_lst_matrix1)):
            pri_vectors.append(num_multiple(par_lst_matrix1[i],mutiple[i]))
        par_lst_matrix = [pri_vectors[0],
                          pri_vectors[1],
                          pri_vectors[2]]
        print(par_lst_matrix)

        # 物质种类（比如：Lu2 Al4）
        y1 = re.findall('Full\sFormula\s(.*?)\n', f1)[0]
        y1_lst = y1.lstrip('(').rstrip(')')
        material = re.findall('Full\sFormula\s(.*?)\n', f1)[0].lstrip('(').rstrip(')')
        self.mat_name = material
        elements = material.split(' ')
        # print(elements)              # (Re4 S8)\(Re108 S216)
        zmb_lst = [chr(i) for i in range(97,123)] + [chr(i) for i in range(65,91)]
        szb_lst = [str(i) for i in range(0,10)]
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
        # print(element_lst)
        # print(number_lst)

        par_lst_species = []                   # 用于Cifwrite参数(species)的
        for i in range(len(element_lst)):
            num = int(number_lst[i])
            for j in range(num):
                par_lst_species.append(element_lst[i])
        print(par_lst_species)



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
        print(par_lst_coords)


        # 构建Structure类
        structure = Structure(par_lst_matrix,par_lst_species,par_lst_coords)
        print(structure)
        slab = CifWriter(structure, write_magmoms=True)   # struct (Structure) – structure to write; symprec (float) – If not none, finds the symmetry of the structure and writes the cif with symmetry information. Passes symprec to the SpacegroupAnalyzer; write_magmoms (bool) – If True, will write magCIF file. Incompatible with symprec
        slab.write_file(r'C:\Users\wang1\Desktop/new_crys/{}.cif'.format(self.mat_name))
        # f = read('/Users/mac/Desktop/crys/{}.cif'.format(self.mat_name))
        # view(f)

# 在底下这个CIF的括号里


# if __name__ == '__main__':
for i in range(2500, 5000):   # to：2511
    try:
        CIF(i).to_cif()
        print(i)
    except:
        pass