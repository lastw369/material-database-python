import sqlite3
import matplotlib.pyplot as plt
from PIL import Image


class Database:
    def __init__(self, db_dir):
        '''
        Database类(已存在的数据库的操作)
        :param db_dir: 数据库路径
        '''
        self.path = db_dir
        self.conn = sqlite3.connect(self.path)
        self.cnn = self.conn.cursor()

    def exhibit_sites(self, content):
        '''
        显示某种材料所有原子种类及坐标
        :param content: 材料的ID或化学式
        :return: None
        '''
        if content.isdigit():
            self.cnn.execute("SELECT Formula from test WHERE ID={0}".format(int(content)))
            formula = self.cnn.fetchone()[0]
        else:
            formula = content
        print("SELECT * FROM {0}".format(formula))
        self.cnn.execute("SELECT * FROM {0}".format(formula))
        # self.cnn.execute()
        for x in self.cnn.fetchall():
            print(x)
        self.conn.commit()

    def exhibit_all_info(self):
        '''
        展示数据库test表格中所有的信息
        :return: None
        '''
        self.cnn.execute("SELECT * FROM test")
        self.conn.commit()
        for x in self.cnn.fetchall():
            print(x)

    def insert_row_into_test(self, ID, formula):
        '''
        插入新的一行在test里
        :param ID: 插入材料的ID
        :param formula: 插入材料的化学式
        :return: None
        '''
        formula = "'" + formula + "'"
        self.cnn.execute('''INSERT INTO test (ID, Formula)  
                            VALUES ({0}, {1})'''.format(ID, formula))
        self.conn.commit()


    def insert_data(self, content, property, data):
        '''
        向test表格中插入或修改数据
        :param content: 需要修改性质的材料的化学式或ID
        :param property: 相应物理性质
        :param data: 数据
        :return: None
        '''
        property = "'" + property + "'"
        if content.isdigit():
            self.cnn.execute("UPDATE test SET {0} = {1} WHERE ID={2}".format(property, data, int(content)))
        else:
            formula = "'" + content + "'"
            self.cnn.execute("UPDATE test SET {0} = {1} WHERE Formula={2}".format(property, data, formula))
        self.conn.commit()

    def delete_row(self, content):
        '''
        用于删除某种材料在数据库(test)中的记录
        :param content: 材料的化学式或者ID
        :return: None
        '''
        if content.isdigit():
            self.cnn.execute("SELECT Formula from test WHERE ID={0}".format(int(content)))
            formula = self.cnn.fetchone()[0]
            self.cnn.execute("DELETE FROM test WHERE ID={0}".format(int(content)))
        else:
            formula = "'" + content + "'"
            self.cnn.execute("DELETE FROM test WHERE Formula={0}".format(formula))
        self.cnn.execute("DROP TABLE {}".format(formula))
        self.conn.commit()

    def delete_data(self, content, property):
        '''
        删除某项数据
        :param content: 材料的化学式或者ID
        :param property: 需要删除的属性
        :return: None
        '''
        if content.isdigit():
            self.cnn.execute("UPDATE test SET {0} = NULL WHERE ID={1}".format(property, int(content)))
        else:
            formula = "'" + content + "'"
            self.cnn.execute("UPDATE test SET {0} = NULL WHERE Formula={1}".format(property, formula))
        self.conn.commit()

    def show_iv(self, content):
        '''
        显示未堆垛材料的IV图像（图像地址需要先用 insert_data函数 存进 test的表格的Image_dir列 下）
        :param content: 材料的ID或化学式
        :return: None
        '''
        if content.isdigit():
            self.cnn.execute("SELECT Image_dir FROM test WHERE ID={}".format(int(content)))
        else:
            formula = "'" + content + "'"
            self.cnn.execute("SELECT Image_dir FROM test WHERE Formula={}".format(formula))
        img_dir = self.cnn.fetchone()[0]
        img = Image.open(img_dir)
        plt.imshow(img)
        plt.show()


    def exhibit_all_info2(self, content):
        '''
        显示某种材料所有堆垛后材料的性质（显示一对多所有情况）
        :param content: 材料（一） 的化学式或ID
        :return: None
        '''
        if content.isdigit():
            self.cnn.execute("SELECT Formula FROM test WHERE ID={0}".format(int(content)))
            formula = self.cnn.fetchone()[0]
        else:
            formula = content
        tbl_name = formula + "_Device"
        self.cnn.execute("SELECT * FROM {}".format(tbl_name))
        self.conn.commit()
        for x in self.cnn.fetchall():
            print(x)

    def insert_data2(self, content, splice_content, property, data):
        '''
        在material_Device表中填入数据
        :param content: 材料的化学式或ID
        :param splice_content: 用于堆垛的材料的化学式或ID
        :param property: 需要更改那一项的名称
        :param data: 更改后的数据
        :return:
        '''
        if content.isdigit():
            self.cnn.execute("SELECT Formula FROM test WHERE ID={0}".format(int(content)))
            formula = self.cnn.fetchone()[0]
        else:
            formula = content
        tbl_name = formula + "_Device"
        if splice_content.isdigit():
            self.cnn.execute("UPDATE {0} SET {1} = {2} WHERE Splice_ID={3}".format(tbl_name, property, data, int(splice_content)))
        else:
            formula = "'" + splice_content + "'"
            self.cnn.execute("UPDATE {0} SET {1} = {2} WHERE Splice={3}".format(tbl_name, property, data, formula))
        self.conn.commit()

    def exhibit_relation(self, content):
        '''
        显示某种材料的所有堆垛信息
        :param content: 材料的ID或化学式
        :return: None
        '''
        if content.isdigit():
            self.cnn.execute("SELECT * FROM relation WHERE ID={}".format(int(content)))
        else:
            self.cnn.execute("SELECT * FROM relation WHERE Formula={}".format("'"+content+"'"))
        for x in self.cnn.fetchall():
            print(x)

    def exhibit_all_relations(self):
        '''
        显示所有材料的所有堆垛情况
        :return: None
        '''
        self.cnn.execute("SELECT * FROM relation ORDER BY ID")
        for x in self.cnn.fetchall():
            print(x)

    def insert_row_into_relation(self, content, splice_content):
        '''
        存入新的堆垛情况
        :param content: 一对多的 一
        :param splice_content: 一对多的 多
        :return: None
        '''

        if content.isdigit():
            self.cnn.execute("SELECT Formula FROM test WHERE ID={0}".format(int(content)))
            formula = self.cnn.fetchone()[0]
            ID = int(content)
        else:
            self.cnn.execute("SELECT ID FROM test WHERE Formula={0}".format("'" + content + "'"))
            formula = content
            ID = self.cnn.fetchone()[0]
        if splice_content.isdigit():
            self.cnn.execute("SELECT Formula FROM test WHERE ID={0}".format(int(splice_content)))
            splice_formula = self.cnn.fetchone()[0]
            splice_ID = int(splice_content)
        else:
            self.cnn.execute("SELECT ID FROM test WHERE Formula={0}".format("'" + splice_content + "'"))
            splice_formula = splice_content
            splice_ID = self.cnn.fetchone()[0]
        self.cnn.execute('''INSERT INTO relation (ID, Formula, Splice_ID, Splice)
                    VALUES ({0}, {1}, {2}, {3})'''.format(ID, "'" + formula + "'", splice_ID,
                                                          "'" + splice_formula + "'"))
        self.conn.commit()

    def insert_data_into_relation(self, content, splice_content, property, data):
        '''
        插入堆垛后材料的性质
        :param content: 材料的化学式或ID
        :param splice_content: 材料的化学式或ID
        :param property: 想要插入数据的性质
        :param data: 数据
        :return: None
        '''
        if content.isdigit():
            ID = int(content)
        else:
            self.cnn.execute("SELECT ID FROM test WHERE Formula={0}".format("'" + content + "'"))
            ID = self.cnn.fetchone()[0]
        if splice_content.isdigit():
            splice_ID = int(splice_content)
        else:
            self.cnn.execute("SELECT ID FROM test WHERE Formula={0}".format("'" + splice_content + "'"))
            splice_ID = self.cnn.fetchone()[0]
        print('''UPDATE relation SET {0}={1}
                            WHERE ID={2} AND Splice_ID={3}'''.format(property, data, ID, splice_ID))
        self.cnn.execute('''UPDATE relation SET {0}={1}
                            WHERE ID={2} AND Splice_ID={3}'''.format(property, data, ID, splice_ID))
        self.conn.commit()

    def delete_row_from_relation(self, content, splice_content):
        '''
        删除某种堆垛情况
        :param content: 材料的化学式或ID
        :param splice_content: 材料的化学式或ID
        :return: None
        '''
        if content.isdigit():
            ID = int(content)
        else:
            self.cnn.execute("SELECT ID FROM test WHERE Formula={0}".format("'" + content + "'"))
            ID = self.cnn.fetchone()[0]
        if splice_content.isdigit():
            splice_ID = int(splice_content)
        else:
            self.cnn.execute("SELECT ID FROM test WHERE Formula={0}".format("'" + splice_content + "'"))
            splice_ID = self.cnn.fetchone()[0]
        self.cnn.execute("DELETE FROM relation WHERE ID={0} AND Splice_ID={1}".format(ID, splice_ID))
        self.conn.commit()

    def delete_data_from_relation(self, content, splice_content, property):
        '''
        删除某种堆垛材料的某个性质
        :param content: 材料的化学式或ID
        :param splice_content: 堆垛材料的化学式或ID
        :param property: 想删除的性质
        :return: None
        '''
        if content.isdigit():
            ID = int(content)
        else:
            self.cnn.execute("SELECT ID FROM test WHERE Formula={0}".format("'" + content + "'"))
            ID = self.cnn.fetchone()[0]
        if splice_content.isdigit():
            splice_ID = int(splice_content)
        else:
            self.cnn.execute("SELECT ID FROM test WHERE Formula={0}".format("'" + splice_content + "'"))
            splice_ID = self.cnn.fetchone()[0]
        self.cnn.execute('''UPDATE relation SET {0}=NULL
                            WHERE ID={1} AND Splice_ID={2}'''.format("'"+property+"'", ID, splice_ID))
        self.conn.commit()

    def show_iv2(self, content, splice_content):
        '''
        显示堆垛后材料的IV图像
        :param content: (一对多的 一)材料的ID或化学式
        :param splice_content: (一对多的 多)材料的ID或化学式
        :return: None
        '''
        if content.isdigit():
            ID = int(content)
        else:
            self.cnn.execute("SELECT ID FROM test WHERE Formula={0}".format("'" + content + "'"))
            ID = self.cnn.fetchone()[0]
        if splice_content.isdigit():
            splice_ID = int(splice_content)
        else:
            self.cnn.execute("SELECT ID FROM test WHERE Formula={0}".format("'" + splice_content + "'"))
            splice_ID = self.cnn.fetchone()[0]
        self.cnn.execute("SELECT Image_dir from relation WHERE ID={} AND Splice_ID={}".format(ID, splice_ID))
        img_dir = self.cnn.fetchone()[0]
        img = Image.open(img_dir)
        plt.imshow(img)
        plt.show()

    def close_db(self):
        '''
        关闭数据库
        :return: None
        '''
        self.conn.close()


if __name__ == "__main__":
    object = Database("/Users/mac/Desktop/crystal.db")
    # object.insert_row_into_relation("3", "5")
    # object.insert_data_into_relation("3", "5", "'Image_dir'", "'/Users/mac/Desktop/MoS2_IV.png'")
    # object.delete_row_from_relation("AgTe4Au", "Ag2F")
    # object.exhibit_all_relations()
    # object.delete_data_from_relation("3", "5", "Schottky_barrier(eV)")
    object.exhibit_all_relations()
    # object.exhibit_all_info2("1")
    # object.exhibit_sites("AgN3")
    # object.insert_row_into_test(91, "O")
    # ID = input("请输入修改数据的材料的ID或化学式：")
    # object.show_iv2("3", "5")
    # object.insert_data2("1", ID, "Image_dir", "/Users/mac/Desktop/MoS2_IV.png")
    # object.exhibit_all_info()
    # material = input("请输入需要删除材料的ID或化学式：")
    # object.delete_row(material)
    # material = input("你要删除那种材料的Schottky_barrier：")
    # object.delete_data(material, 'Schottky_barrier(eV)')
    # object.exhibit_all_info()
    object.close_db()
