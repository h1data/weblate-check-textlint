# Weblate独自チェック開発者向け情報

ここでは、ドキュメントには記載されていない機能を実現するための実装方法について補足します。
Weblate本体の仕様変更で使用できなくなる場合があるため、予めご了承ください。

## 翻訳フラグにより独自チェックを有効化、無効化したい場合
作成した独自チェックを特定のプロジェクトや言語コンポーネントでのみ使用したい場合、
プロジェクトやコンポーネントの翻訳フラグで有効・無効を切り替えられます。
この動作はチェッククラスのクラス変数`default_disabled`に`True`を設定するだけで実現できます。

``` python
class TextlintCheck(TargetCheck):
    """ check for a translation unit with textlint """
    default_disabled = True
    check_id = "check_textlint"
```

基底チェッククラスBaseCheckにより、翻訳フラグ存在チェックの中でcheck_idに指定した`check_textlint`のアンダースコアをハイフンに変換した、`check-textlint`が独自チェックを有効化する翻訳フラグとして使用されます。

## descriptionを動的に変更したい場合

独自チェッククラスでget_description(self, check_obj)を実装します。

## コメントを登録したい場合

scopeとnameから`check:textlint`というユーザー名のボットを自動的に追加し、ボット名義のコメントをチェック対象の翻訳文に追加します。
``` python
    # deferred importing ORM class
    from weblate.auth.models import User
    from weblate.trans.models import Comment
    # ...
    Comment.objects.create(
        comment = "コメント文字列",
        user = User.objects.get_or_create_bot(
            scope="check",
            name="textlint",
            verbose="texlint check",
        ),
        unit = unit
    )
```
User、Commentクラスをファイル先頭でimportすると、settings-override.pyで独自チェッククラスのオブジェクトを生成する時点でDjangoはモデルクラスを使用する準備ができていないため実行時エラーとなる場合があります。この場合は、チェック処理の中でimportする必要があります。
