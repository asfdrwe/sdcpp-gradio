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
| Windows + Ryzen 5600 + Geforce 3060 12GB | 30秒〜1分（初回はモデルがキャッシュされていないので+1分) |
| M4 Mac mini | 2 分 |
| Linux Fedora 42 + Ryzen 5600G (内蔵GPU) | 6分 |
| Linux Fedora 42 + Core i7100 (内蔵GPU) | VAE デコード時にエラーが出る |
| Linux Fedora 42 + Core i7100 + RX 470 8GB |  2分半 |

x86_64 の場合、使用している pytorch が AVX 前提なので、 AVX 非対応の第1世代
(Nehalem)以前の Core i、第10世代(Comet Lake)以前の Celeron, Pentium、 Atom では
動かないと思います。

## 実行プログラム

- sdcpp-gradio-safe.exe
こちらは一般向け画像のみが生成されます。日本語から英語プロンプトを生成する段階と
英語プロンプトから画像を生成する段階の両方で一般向けになるよう制限がかかります。

- sdcpp-gradio.exe
こちらはセンシティブ設定(4段階)が可能です。センシティブ設定を右にすればするほど
より性的な画像が生成されます。生成画像の扱いに気をつけてください。

どちらも著作権が存在するキャラク生成に対する制限は行っていません。
生成画像の利用についてについて私的使用の例外(著作権法第30条)の範囲を超える場合は、
著作権法に反しないよう心がけてください。

文化庁の資料 [AIと著作権について](https://www.bunka.go.jp/seisaku/chosakuken/aiandcopyright.html)

### インストール
Hugging Faceから[zipファイル](https://huggingface.co/asfdrwe/waiDMD2/resolve/main/sdcpp-gradio-windows.zip?download=true)をダウンロードし、
ダウンロードしたファイルを右クリックで展開してください。

### 実行
sdcpp-gradio フォルダを開き、sdcpp-gradio-safe.exe もしくは sdcpp-gradio.exe をダブルクリックしてください。

Windows ターミナルが起動し、自動的にブラウザが開かれます。

『生成した画像を日本語の文章で入力』欄に生成したい画像を文章でいれてください。

例: 少女が微笑む画像。

解像度を選んでください。

生成を押ししばらくすると右の『output』に画像が生成されます。生成されたファイルは
sdcpp-gradio フォルダの output フォルダに『年月日時分秒.png』形式(例: 20250514192813.png)で保存されます。

### 終了方法
ブラウザを閉じ、Windowsターミナルを閉じてください。

### うまく動かない場合
sd-master-10feacf-bin-win-avx2-x64 フォルダに CPU 用 stable-diffusion.cpp があるので、
sd.exe と stable-diffusion.dll を sdcpp-gradio フォルダに上書きコピーして
Vulkan 版から差し替えてください。CPU 用なら生成時間がかかりますが動くはずです
(Ryzen 5600 で 12 分、Core i7100 で36分かかりました)

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
