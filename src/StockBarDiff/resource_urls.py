import sys

ROOT_URL = sys.path[0]
DATA_ROOT_URL = ROOT_URL + '\data'
DATA_LINE_URL = DATA_ROOT_URL + '\line'
DB_SQLITE_PATH = 'StockBarDiff\\db.sqlite3'
# local stock symbol config path
STOCK_SYMBOL_FILE = DATA_ROOT_URL + '\stock_code.txt'
# web address
WEB_URL = 'http://d.10jqka.com.cn/v2/line/hs_%s/%s/%s.js'  # symbol  00 No, 01 before, 02 later  year

def test() -> object:
    print(ROOT_URL)
    print(DATA_ROOT_URL)
    print("STOCK_SYMBOL_FILE : ", STOCK_SYMBOL_FILE)

if __name__ == '__main__':
    # main()
    test()
