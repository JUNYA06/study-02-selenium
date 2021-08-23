#ログ出力について、どのような観点で出力したら良いかわからず記載できませんでした。
#これから回答を見て、復習します。


import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

import time
import pandas as pd
import sys
import logging
import datetime
from webdriver_manager.chrome import ChromeDriverManager

#相対パスで書くこと
LOG_FILE_PATH = "./log/log_{datetime}.log"
EXP_CSV_PATH = "./exp_list_{search_keyword}_{datetime}.csv"
log_file_path = LOG_FILE_PATH.format(datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))


# Chromeを起動する関数
args = sys.argv

log_fmt = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_fmt, level=logging.ERROR)

def export_csv(list):
    list.to_csv("list.csv")

# def setup_class(cls):
#     cls.driver = webdriver.Chrome(ChromeDriverManager().install())

def set_driver(driver_path, headless_flg):
    
    
    if "chrome" in driver_path:
          options = ChromeOptions()
    else:
      options = Options()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    driver_path = ChromeDriverManager().install()
    if "chrome" in driver_path:
        # return Chrome(executable_path=os.getcwd() + "/" + driver_path,options=options)
        return Chrome(driver_path,options=options)
    else:
        return Firefox(executable_path=os.getcwd()  + "/" + driver_path,options=options)

def log(txt):
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr = '[%s: %s] %s' % ('log',now,txt)

    with open(log_file_path,'a',encoding='utf-8_sig')as f:
        f.write(logStr + '\n')
    print(logStr)



# main処理

def main():
    log("処理開始")

    search_keyword = args[1]
    if search_keyword is None:
        print("第一引数に検索ワードを入れてください！")
    log("検索ワード:{}".format(search_keyword))
        
    # 08/21 修正 driverのバージョンアップ 
    # setup_class()
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    try:
    # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass

    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # ページ終了まで繰り返し取得
    # 検索結果の一番上の会社名を取得

    
    # 空のDataFrame作成
    df = pd.DataFrame()

    exp_name_list = []
    exp_copy_list = []
    exp_status_list = []
    exp_first_year_fee_list = []
    count = 0
    sucess = 0
    fail = 0

    while Ture:
    # 1ページ分繰り返し
        for a in range(2):
            
            name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
            paying_list = driver.find_elements_by_class_name("tableCondition__body")
            # status_list = driver.find_elements_by_class_name("tableCondition__body")
            # table_list = driver.find_elements_by_class_name("tableCondition__body")

            print(len(name_list))
            for name,paying in zip(name_list,paying_list):
                print(name.text)
                # DataFrameに対して辞書形式でデータを追加する
                df = df.append(
                    {"会社名": name.text, 
                    "給料": paying.text}, 
                    ignore_index=True)
            driver.execute_script('document.querySelector(".karte-close").click()')
            time.sleep(5)
            driver.find_element_by_class_name("pager__next").click()
            time.sleep(5)
            logging.info('')

        export_csv(df)
        logging.basicConfig(filename='example.log', format=log_fmt)
        


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
