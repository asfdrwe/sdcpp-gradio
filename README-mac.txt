# sdcpp-gradio 日本語画像生成ツール

日本語文章から英語プロンプトを作成する[danbot](https://zenn.dev/platina/articles/66ac45608c836e)と
Stable Diffusionで英語プロンプトから画像を生成する[stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp)と
簡単にWebインターフェースを作成できる[gradio](https://www.gradio.app/)を
組み合わせて、日本語文章から画像生成するアプリを作成しました。

日本語で文章を入力し、解像度を選び、生成ボタンを押すだけで画像を生成できます。

Vulkan バックエンドなので生成は少し遅いですが、nvidia のグラフィックボードだけでなく 
AMD や Intel のグラフィックボードや CPU 内蔵 GPU などでも動作する可能性があります。

メモリに関しては GGUF形式 Q4_K 量子化でモデルを圧縮しているので、省メモリで生成
できます。外付け GPU なら VRAM 4GB、メインメモリ共有の内蔵 GPU では 8 GBの
メインメモリがあれば足りると思います。

## 動作環境と生成時間の目安

| 動作環境         | 時間 |
|--------------|------|
| M4 Mac mini | 2 分 |

## 実行プログラム

- sdcpp-gradio-safe
こちらは一般向け画像のみが生成されます。日本語から英語プロンプトを生成する段階と
英語プロンプトから画像を生成する段階の両方で一般向けになるよう制限がかかります。

- sdcpp-gradio
こちらはセンシティブ設定(4段階)が可能です。センシティブ設定を右にすればするほど
より性的な画像が生成されます。生成画像の扱いに気をつけてください。

どちらも著作権が存在するキャラク生成に対する制限は行っていません。
生成画像の利用についてについて私的使用の例外(著作権法第30条)の範囲を超える場合は、
著作権法に反しないよう心がけてください。

文化庁の資料 [AIと著作権について](https://www.bunka.go.jp/seisaku/chosakuken/aiandcopyright.html)

## インストール
[zipファイル](https://huggingface.co/asfdrwe/waiDMD2/resolve/main/sdcpp-gradio-mac.zip?download=true)をダウンロードしてください。

Finderでダウンロードフォルダのsdcpp-gradio-macフォルダを開きます。

拡張属性削除.workflowをダブルクリックしてインストールしてください。

Finderで上のフォルダに戻り、sdcpp-gradio-macフォルダの上で右クリックし、クイックアクションの拡張属性削除を選び、検疫を解除してください。

### 実行
sdcpp-gradio-mac フォルダを開き、sdcpp-gradio-safe.command もしくは sdcpp-gradio.command をダブルクリックしてください。

ターミナルが起動し、自動的にブラウザが開かれます。

(検疫属性を削除していない場合、警告が出て実行できないので、
システム設定のプライバシーとセキュリティから実行を許可し
もう一度ダブルクリックしてください)

『生成した画像を日本語の文章で入力』欄に生成したい画像を文章でいれてください。

例: 少女が微笑む画像。

解像度を選んでください。

生成を押ししばらくすると右の『output』に画像が生成されます。生成されたファイルは
sdcpp-gradio フォルダの output フォルダに『年月日時分秒.png』形式(例: 20250514192813.png)で保存されます。

### 終了方法
ブラウザを閉じ、ターミナルを閉じてください。

### 注

stable-diffusion.cpp には Metal Performace Shader(MPS)対応版もありますが、
2025/5/16時点では遅く、Vulkan の方が 4 倍以上速いです。MPS版を動かしたい場合は
sdcpp-gradio-macフォルダ内のsdをどこかに移動させ、sd-mpsをsdに変更してください。

## 著作権

Copyright (c) 2025 asfdrwe <asfdrwe@gmail.com>

[Apache License 2.0](LICENSE)

日本語から英語変換部分は
[Plat氏のコード](https://zenn.dev/platina/articles/66ac45608c836e)から流用しています。
ライセンスは[おそらく Apache License 2.0](https://github.com/p1atdev/danbooru-tags-translator-web-app/LICENSE) なので
自分のコードも Apache License 2.0 とします。

stable-diffusion.cpp の呼び出し部分は
[GradioStableDiffusionCPP](https://github.com/fabiomatricardi/GradioStableDiffusionCPP) を
参考にしています。

Windows 版と macOS 版に 同梱している stable-diffusion.cpp のライセンスは
[MIT License](https://github.com/leejet/stable-diffusion.cpp/blob/master/LICENSE)で、
含まれる ggml も[MIT License](https://github.com/ggml-org/ggml/blob/master/LICENSE)です。

同梱しているモデル waiNSFWIllustrious_v140_DMD2_Q4_K.gguf はマージ元の
wai-nsfw-illustrious-sdxl と DMD2 のライセンスに従います。
DanbotNL 2408 260M のライセンスは DanbotNL のライセンスに従います。

- [Plat](https://huggingface.co/dartags/DanbotNL-2408-260M)
- [fabiomatricardi](https://github.com/fabiomatricardi/GradioStableDiffusionCPP)
- [leejet](https://github.com/leejet/stable-diffusion.cpp)
- [ggml](https://github.com/ggml-org/ggml)
- [WAI0731](https://civitai.com/models/827184/wai-nsfw-illustrious-sdxl)
- [tanweiy](https://huggingface.co/tianweiy/DMD2)
