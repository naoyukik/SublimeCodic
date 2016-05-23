codicのAPIを使用したSublime Text 3 用のプラグインです。  
codic公式サイト: [https://codic.jp/](https://codic.jp/)


# 使い方
- フレーズを選択しながら codic_translate_string コマンドを呼び出した場合、選択した文字列をAPIへ投げて、翻訳後の文字列に置き換えます。
- 何も選択せずに codic_translate_string コマンドを呼び出した場合、ウィンドウ下部にinputパネルが出ますのでそこから入力して翻訳します。文字列はカーソル位置に挿入されます。
- Project IDは codic_get_project_ids を呼び出して確認したIDをキーコンフィグで設定して使用します(設定方法は下記参照)。

# インストール
現在のところ、Package Controlに対応していません。  
BitbucketからMercurialを使用してSublime Text 3のPackages配下にDLしてください。

``` bash
$ hg clone ssh://hg@bitbucket.org/dat/sublimecodic
```

# キーバインド

``` json
{
  "keys": ["alt+d"], "command": "codic_translate_string", "args": {"casing": "camel"},
  "keys": ["alt+t"], "command": "codic_translate_string", "args": {"casing": "camel", "acronym_style": "camel strict"},
  "keys": ["alt+p"], "command": "codic_translate_string", "args": {"casing": "camel", "acronym_style": "camel strict", "project_id": "0"},
}
```

# セッティング

``` json
{
    "access_token": "codicサイトから取得した自分のアクセストークン",
    "casing": "camel",
    "acronym_style": "camel strict"
}
```

# よくある質問
Q. コンソールにエラーがなんか出てる  
A. エラー処理皆無なので何かあったら連絡ください。

Q. 使ってたら突然何も起きなくなった。  
A. もしかしたらAPIの制限回数に達してるかもしれません。codicサイトへ行って確認してください。

# 謝辞
codicという開発者に素晴らしいサイトを公開していただき誠にありがとうございます。  
また、このプラグインは airtoxin様のcodic-sublime を参考にさせていただきました。誠にありがとうございます。
airtoxin様のcodic-sublime: [https://github.com/airtoxin/codic-sublime](https://github.com/airtoxin/codic-sublime)
