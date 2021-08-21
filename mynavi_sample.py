import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import sys
import logging

# Chromeを起動する関数
args = sys.argv

log_fmt = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_fmt, level=logging.ERROR)

def export_csv(list):
    list.to_csv("list.csv")

def setup_class(cls):
    cls.driver = webdriver.Chrome(ChromeDriverManager().install())

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
    if "chrome" in driver_path:
        return Chrome(executable_path=os.getcwd() + "/" + driver_path,options=options)
    else:
        return Firefox(executable_path=os.getcwd()  + "/" + driver_path,options=options)

# main処理

def main():

    search_keyword = args[1]
    # 08/21 修正 driverのバージョンアップ 
    setup_class()
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')

    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # ページ終了まで繰り返し取得
    # 検索結果の一番上の会社名を取得

    
    # 空のDataFrame作成
    df = pd.DataFrame()


    # 1ページ分繰り返し
    for a in range(2):
        try:
            name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
            paying_list = driver.find_elements_by_class_name("tableCondition__body")

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
        except:
            pass
    export_csv(df)
    logging.basicConfig(filename='example.log', format=log_fmt)
        


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
