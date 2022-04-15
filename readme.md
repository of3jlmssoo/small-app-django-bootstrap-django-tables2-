## アプリケーション概要

申請者がお買い物を申請する。承認者が承認したり差し戻したりする。

## ユーザー(申請者)処理

![userProcess](docs/userProcess.drawio.svg)

## 承認者処理

![approverProcess](docs/approverProcess.drawio.svg)

## テーブル

![usersTables](docs/usersTables.drawio.svg)

## モデル

![model](docs/model.drawio.svg)

## ログイン

メールアドレスでログイン。認証は django 任せ。メールアドレス登録時承認者かどうかセットする。登録されたメールアドレスにメールが送付され確認を求める。確認が取れてから使えるようになる。

## ユーザーインターフェース例

### ログイン直後の画面

申請者がログインした直後の画面。
![model](docs/dashboard.png)
承認者の場合、表示されるのは『申請済み』と『承認済み』のみ。

### 申請画面

承認者用申請画面。申請 ID とコメントは編集できない。申請 ID は新規申請の場合ブランク。保存するか申請すると ID が割り振られ表示されるが編集はできない。コメントを編集できるのは承認者のみ。
![model](docs/applicatonForm.png)

## その他

django、bootstrap、django-tables2、django-bootstrap-modal-forms を使っている。
物品名については e-Stat の『日本標準商品分類(平成 2 年[1990 年]6 月改定)』のデータをダウンロードし(FEK_download.csv)、その中からランダムに商品名を表示するプログラムを作り参考にしている。
最初に bootstrap で画面を作成し、イメージができたところで django 機能を組み込んだ。
