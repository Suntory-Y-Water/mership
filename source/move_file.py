import os
import shutil
from datetime import datetime

def move_ship_list():
    # ファイルの移動先ディレクトリ
    destination_folder = "../old_ship_lists"

    # ファイル名に使用する現在の日時を取得
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    try:
        # 移動先フォルダが存在しない場合は作成
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # ファイルを移動し、リネーム
        shutil.move("../output.csv", os.path.join(destination_folder, f"shippedList_{timestamp}.csv"))
        return "ファイルの移動とリネームが完了しました。"
    except FileNotFoundError:
        return "エラー: 指定されたファイルが見つかりません。"
    except PermissionError:
        return "エラー: ファイルやディレクトリへのアクセス権限がありません。"
    except shutil.Error:
        return "エラー: ファイルの移動に失敗しました。同じ名前のファイルがすでに存在するか、その他の問題が発生している可能性があります。"
    except Exception as e:
        return f"エラー: 予期しないエラーが発生しました。詳細: {str(e)}"