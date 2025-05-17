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
| Windows + Ryzen 5600 + Geforce 3060 12GB | 30秒〜1分 |
| M4 Mac mini | 2 分 |
| Linux Fedora 42 + Ryzen 5600G (内蔵GPU) | 6分 |
| Linux Fedora 42 + Core i7100 (内蔵GPU) | VAE デコード時にエラーが出る |
| Linux Fedora 42 + Core i7100 + RX 470 8GB |  2分半 |

x86_64 の場合、使用している pytorch が AVX 前提なので、 AVX 非対応の第1世代
(Nehalem)以前の Core i、第10世代(Comet Lake)以前の Celeron, Pentium、 Atom では
動かないと思います。

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

## Windows 版

### インストール
[zipファイル](https://huggingface.co/asfdrwe/waiDMD2/resolve/main/sdcpp-gradio.zip?download=true)をダウンロードし、
ダウンロードしたファイルを右クリックで展開してください。

### 実行
sdcpp-gradio フォルダを開き、sdcpp-gradio-safe.exe もしくは sdcpp-gradio.exe をダブルクリックしてください。

実行の際にWindowsによってPCが保護されましたという警告が出る場合がありますが、そのまま詳細情報を
押して実行を押してください。

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

## macOS 版

### インストール
zipファイルをダウンロードし、ダウンロードしたファイルを右クリックで展開してください。

そのままでは GateKeeper によるセキュリティチェックに引っかかるので、
こちらのツールで検疫属性を削除してください。

### 実行
sdcpp-gradio フォルダを開き、sdcpp-gradio-safe.command もしくは sdcpp-gradio.command を
ダブルクリックしてください。

ターミナルが起動し自動的にブラウザが開かれます。
(検疫属性を削除していない場合、警告が出て実行できないので、設定から実行を許可し
もう一度ダブルクリックしてください。)

あとはWindows版と同じように操作することで画像を生成できます。

#### 終了
ブラウザを閉じ、ターミナルを閉じてください。

## Linux
あらかじめgit と gcc 等の開発ツールと Vulkan 開発環境をインストールして
ください(Fedoraなら`dnf install vulkan-headers`等)。

git で本体をダウンロードしてください。

```
git clone https://github.com/asfdrwe/sdcpp-gradio
cd sd-gradio
```

[stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp)の
指示に従い stable-diffusion.cpp を Vulkan 対応でビルドします。

```
git clone https://github.com/leejet/stable-diffusion.cpp
cd stable-diffusion.cpp
git submodule init
git submodule update
mkdir build
cmake .. -DSD_VULKAN=ON 
cmake --build . --config Release -j
```

生成された実行ファイルのsd を sdcpp-gradio フォルダに移動させてください。

Windows 版か macOS 版 をダウンロードし、右クリックで展開し、DanbotNL-2408-260M
フォルダと waiNSFWIllustrious_v140_DMD2_Q4_K.gguf  を sdcpp-gradio フォルダに
移動させてください。

python の仮想環境を作ります。

```
python -m venv venv
. venv/bin/venv
```

必要なモジュールをインストールします。

```
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

### 実行

```
python sd-gradio-safe.py
```

または

```
python sd-gradio.py
```

で実行してください。

あとはWindows版と同じように操作することで画像を生成できます。

## macOS でのビルド

コマンドライン版 xcode と brewをインストールしてください。

```
xcode-select install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

brew を実行するのに必要な設定を行います。
```
echo >> $HOME/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> $HOME/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```


[Vulkan 参考ページ](https://tatsy.github.io/blog/applications/graphics/1609/)を参考に
brew でNoVulkan の開発環境をインストールします。

```
brew install vulkan-headers glslang molten-vk shaderc
```

本体をダウンロードします。

```
git clone 
cd sd-gradio
```

python の仮想環境を作ります。

```
python3 -m venv venv
. venv/bin/venv
```

必要なモジュールをインストールします。

```
pip install torch
pip install -r requirements.txt
```

stable-diffusion.cpp を Vulkan 対応でビルドします。

```
git clone https://github.com/leejet/stable-diffusion.cpp
cd stable-diffusion.cpp
git submodule init
git submodule update

mkdir build
cd build
cmake .. -DSD_VULKAN=ON -DSD_METAL=OFF -DVulkan_INCLUDE_DIR=/opt/homebrew/include -DVulkan_
LIBRARY=/opt/homebrew/lib/libMoltenVK.dylib 
cmake --build . --config Release -j
```

bin/以下にビルドされた実行ファイルのsd を sd-gradio フォルダにコピーしてください。

```
cp bin/sd ../../
cd ../../
```

### macOS 用追加作業
このままでも動きますが、実行ファイル sd の libMoltenVK.dylib へのリンクのパスが
`/opt/homebrew/opt/molten-vk/lib/libMoltenVK.dylib` になっているので、
そのままではそこにlibMoltenVK.dylibがないと動作しません。

このままでは配布しづらいので、実行ファイル sd と同じ場所に libMoltenVK.dylib を
置き、リンク修正します。

`libMoltenVK.dylib` を sd-gradio フォルダにコピーしてください。

```
cp /opt/homebrew/opt/molten-vk/lib/libMoltenVK.dylib ./
install_name_tool -add_rpath @executable_path sd
install_name_tool -change /opt/homebrew/lib/libMoltenVK.dylib @rpath/libMoltenVK.dylib sd
```

otool で正しいパス(@rpath/libMoltenVK.dylib)でリンクしているか確認してください。

```
otool -L sd
sd:
        /System/Library/Frameworks/Accelerate.framework/Versions/A/Accelerate (compatibility version 1.0.0, current version 4.0.0)
        /System/Library/Frameworks/Foundation.framework/Versions/C/Foundation (compatibility version 300.0.0, current version 3423.0.0)
        /System/Library/Frameworks/Metal.framework/Versions/A/Metal (compatibility version 1.0.0, current version 368.11.4)
        /System/Library/Frameworks/MetalKit.framework/Versions/A/MetalKit (compatibility version 1.0.0, current version 168.6.0)
        /usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1351.0.0)
        @rpath/libMoltenVK.dylib (compatibility version 1.0.0, current version 1.0.0)
        /usr/lib/libc++.1.dylib (compatibility version 1.0.0, current version 1900.178.0)
```

[参考サイト](https://yubeshicat.hatenablog.com/entry/2021/12/30/160748)

## Pyinstallerでの実行ファイル化

### specファイル作成
git には最初から入れてありますが、作成する場合は次のコマンドを実行してください。

```
pyi-makespec --onefile --collect-data gradio_client --collect-data safehttpx --collect-data groovy --collect-data gradio sdcpp-gradio-safe.py
pyi-makespec --onefile --collect-data gradio_client --collect-data safehttpx --collect-data groovy --collect-data gradio sdcpp-gradio.py
```

specファイルを編集して
```
...
    excludes=[],
    noarchive=False,
    optimize=0,
)
...
```

を

```
...
    excludes=[],
    noarchive=False,
    optimize=0,
    module_collection_mode={
        'gradio': 'py',  # Collect gradio package as source .py files
    },
)
...
```
に変更します((参考)[https://github.com/pyinstaller/pyinstaller/issues/8108])。

次のコマンドを実行してください。

```
make all
```

これで dist フォルダ以下に sdcpp-gradio と sdcpp-gradio-safe が生成されます。

### 注

stable-diffusion.cpp には Metal Performace Shader(MPS)対応版もありますが、
2025/5/16時点では遅く、Vulkan の方が 4 倍以上速いです。

macOS + python 3.10, 3.11, 3.12 + Pyinstaller ではブラウザを起動しつづけるバグがあります。
なので、Pyinstallerを使わず、ポータブル版のPythonを同梱しています。

[stable-diffusion-cpp-python](https://github.com/william-murray1204/stable-diffusion-cpp-python)という Python モジュール経由で
生成する方法もあります。
ただ、Fedora 42 + Ryzen 5600G + Vulkan で試したところ、繰り返し画像生成すると
2回目以降生成画像がおかしくなる問題があったので、使用していません。

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
