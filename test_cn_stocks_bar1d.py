import os
import unittest
import pandas as pd

class TestStockIndexBar1d(unittest.TestCase):

    """Get test data"""

    @classmethod
    def setUpClass(cls) -> None:
        cls._indexbar1ddata = cls.get_indexbar1ddata()
        cls._indexinfodata = cls.get_indexinfodata()

    @classmethod
    def tearDownClass(cls) -> None:
        del cls._indexbar1ddata

    @classmethod
    def get_indexbar1ddata(cls) -> pd.DataFrame:
        df = pd.read_csv('cn_stock_index_bar1d.csv')
        if df.empty:
            raise ValueError("No test data available")
        return df

    @classmethod
    def get_indexinfodata(cls) -> pd.DataFrame:
        df = pd.read_csv('cn_stock_index_info.csv')
        if df.empty:
            raise ValueError("No test data available")
        return df

    def error_msg(self, msg: str) -> str:
        return f"[cn_stock_index_bar1d] - {msg}"

    def result_test(self, df, msg: str):
        if not df.empty:
            self.assertTrue(
                False,
                self.error_msg(
                    msg + f"{df.head(1).to_string()}\n" + f"Total rows: {df.shape[0]}"
                ),
            )

    def result_csv(self, df, str_msg, title):
        cwd = os.getcwd()
        df.to_csv(f"{cwd}/{title}.csv", index=False, mode="w")
        self.result_test(df, title + " : " + str_msg)

    def test_alldata(self):
        """Test overall data in the table"""
        if self._indexbar1ddata.empty:
            self.assertTrue(
                False,
                self.error_msg(f"No data available from {'2023-08-03'} to {'2023-08-15'}"),
            )
        else:
            self.result_test(
                self._indexbar1ddata, f"Data from {'2023-08-03'} to {'2023-08-15'}:\n"
            )

    def test_data_isnot_null_or_illegal(self):
        """Test if data is missing, contains null values, or illegal values (test01)"""
        title = "test_data_isnot_null_or_illegal"
        df_index_bar1d = self._indexbar1ddata.copy()
        df_result01 = df_index_bar1d[df_index_bar1d.isnull().any(axis=1)]
        cols = df_index_bar1d.columns.to_list()
        df_result02 = pd.DataFrame()
        for col in cols:
            df_result03 = df_index_bar1d[
                df_index_bar1d[col].astype(str).str.contains("/")
            ]
            df_result02 = pd.concat([df_result02, df_result03])

        df_result = pd.concat([df_result01, df_result02])
        self.result_csv(df_result, "Data values are missing or illegal:\n", title)

    def test_high_ishigher_low(self):
        """Test if daily high prices are lower than low prices (test02)"""
        title = "test_high_ishigher_low"
        df_index_bar1d = self._indexbar1ddata.copy()
        df_result = df_index_bar1d[df_index_bar1d["high"] < df_index_bar1d["low"]]
        self.result_csv(df_result, "Stocks have daily high prices lower than low prices:\n", title)

    def test_changeratio_below_1(self):
        """Test if change ratios exceed 1 (test03)"""
        title = "test_changeratio_below_1"
        df_index_bar1d = self._indexbar1ddata.copy()
        df_result = df_index_bar1d[abs(df_index_bar1d["change_ratio"]) >= 1]
        self.result_csv(df_result, "Stocks have change ratios exceeding 1:\n", title)

if __name__ == "__main__":
    unittest.main()
