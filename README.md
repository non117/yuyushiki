yuyushiki
=========

Yuyushiki Annotation tool

依存関係
==========
* Python 3.4 or higher.
* jinja2
* flask ( cgiではアレかもわからん )

仕様
==========
1. 設定で指定したディレクトリを再帰的に見ます
2. 画像のあるディレクトリで作業します
3. 画像とフォームをブラウザに表示します
4. タグ付け等アノテーションをしてもらいます
5. 次の画像へ移動したら、データを記録しておきます

データ形式
----------------
JSONを出力

* 画像のファイル名(ディレクトリも？)
* 台詞文字列
* [人物タグ]

UI
----------------
* 台詞は人間ががんばって入力する
* 人物タグは補完ができるようにすると良いかも
* ↑ あるいはシステム側にタグとして持たせておく
* キーボードショートカットを実装しておく
* 画面遷移だるいのでajaxか何か

その他
----------------
* アノテーションしたデータが飛ぶとつらいので逐次書き出し
* データができたらランダム4コマシステムに応用します
