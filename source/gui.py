import os
import time
import PySimpleGUI as sg
from tkinter import messagebox
from logmaster import WriteLogger
from scraper import MercariScraper

class GUI(MercariScraper):

    font = ("Meiryo UI", 16)

    def __init__(self):
        super().__init__()
        self.record = WriteLogger()
        self.record.logger.info("-----------------------------")
        self.record.logger.info("　　　 　　　Start　　 　　　　")
        self.record.logger.info("-----------------------------")


    # 発送する商品を取得するレイアウト
    def get_layout(self) -> list:
        layout = [[sg.Text("発送する商品を自動で取得するプログラムです\n\n必ずタスクマネージャーからMicrosoft Edgsのタスクを終了させてください\n", font=self.font)],
                [sg.Button('商品を取得', key='-GET-', font=self.font)]]
        return layout

    # 発送ボタンを押下するレイアウト
    def ship_layout(self) -> list:
        layout = [[sg.Text("自動で発送通知を押下するプログラムです\n\n全ての発送が終了後に実施してください\n", font=self.font)],
                [sg.Button('発送を通知する', key='-ship-', font=self.font)]]
        return layout
    
    # メインウィンドウのレイアウト
    def layout(self) -> list:
        get_data_layout = self.get_layout()
        ship_layout = self.ship_layout()
        layout = [[sg.Text('業務を選択してください。', font=self.font)],
                [sg.TabGroup([[sg.Tab('商品情報取得', get_data_layout),
                                sg.Tab('発送通知', ship_layout)]], key='-TABGROUP-', enable_events=True, font=self.font)]]    
        return layout

    def main(self):
        scraper = MercariScraper()

        sg.theme('DarkGray15')
        window = sg.Window('自動発送アプリ', self.layout())

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED:
                self.record.logger.info("-----------------------------")
                self.record.logger.info("　　　 　　　 end 　　 　　　　")
                self.record.logger.info("-----------------------------")
                break

            if event == '-GET-':
                scraper.init_driver()
                self.record.logger.info("商品情報を取得中...")
                shipping_url = scraper.get_shipping_dict()

                file_name = "../output.csv"
                if os.path.exists(file_name):
                    os.remove(file_name)

                for url in shipping_url:
                    info = scraper.get_buyer_information(url)
                    self.record.logger.info(info)
                    time.sleep(2)
                    scraper.add_to_csv(*info[0:])
                scraper.quit()

                messagebox.showinfo("終了通知", "発送する商品情報を取得しました\n宛名作成.lbxを開いて内容を確認してください")

            if event == '-ship-':
                if messagebox.askquestion("確認", "本当に全て発送しましたか？\n発送しない商品はCSVファイルから削除してください") == "yes":
                    self.record.logger.info("全ての商品を発送します")
                    self.record.logger.info("発送後はlogファイルのlog.txtをご確認ください")

                    scraper.init_driver()
                    
                    urls = scraper.read_csv_column_f("../output.csv")

                    # URLに遷移し、処理を行う
                    scraper.process_urls(urls)
                    scraper.quit()
                    messagebox.showinfo("終了通知", "発送が完了しました")

        window.close()


if __name__ == '__main__':
    gui = GUI()
    gui.main()