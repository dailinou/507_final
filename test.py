import unittest
from final2 import *
from final import *


class Test(unittest.TestCase):
    def test_data_access(self):
        self.assertEqual(len(steam_top_names_list), 25)
        self.assertEqual(steam_top_names_list[0],'Halo: The Master Chief Collection')
        self.assertEqual(steam_top_url_list[2],'https://store.steampowered.com/app/1174180/Red_Dead_Redemption_2/?snr=1_7_7_topsellers_150_1')
        self.assertEqual(steam_top_names_list[2],'Red Dead Redemption 2')

    def test_storage(self):
        conn = sqlite.connect(sql_file_name)
        cur = conn.cursor()

        sql = 'SELECT Developer_name FROM Developers'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 106)
        self.assertEqual(result_list[0][0],None)
        self.assertEqual(result_list[2][0],'Rockstar Games ')
        self.assertEqual(result_list[3][0],'343 Industries')
        sql = 'SELECT Game_name FROM Games'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(result_list[0][0],'Halo: The Master Chief Collection')




    def test_processing(self):
        conn = sqlite.connect(sql_file_name)
        cur = conn.cursor()

        sql = 'SELECT Developer_name,Toatl_review FROM Developers'
        results = cur.execute(sql)
        result_list = results.fetchall()
        name_list = []
        review_list = []
        for i in result_list:
            name_list.append(i[0])
            review_list.append(i[1])
        self.assertEqual(review_list[23],946)
        self.assertEqual(name_list[23],'Re-Logic ')
        self.assertEqual(review_list[54],79)
        self.assertEqual(name_list[54],None)
        self.assertEqual(review_list[100],1130)
        self.assertEqual(name_list[100],'Behaviour Digital Inc. ')







if __name__ == "__main__":
	unittest.main(verbosity=2)
