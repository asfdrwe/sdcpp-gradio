# SPDX-License-Identifier: Apache License 2.0

import gradio
import torch
from transformers import AutoModelForPreTraining, AutoProcessor
from datetime import datetime
import subprocess
from PIL import Image
import os

if os.name == 'nt':
    SD='sd.exe'
elif os.name == 'posix':
    SD='./sd'

# REPO = "dartags/DanbotNL-2408-260M"

REPO = "./DanbotNL-2408-260M"
processor = AutoProcessor.from_pretrained(REPO, trust_remote_code=True, revision="f992aa6")
model = AutoModelForPreTraining.from_pretrained(REPO, trust_remote_code=True, torch_dtype=torch.bfloat16, revision="f992aa6")

def generate(prompt, sensitive, resolution):
    if sensitive >= 3.0:
        rating = "explicit"
    elif sensitive >= 2.0:
        rating = "questionable"
    elif sensitive >= 1.0:
        rating = "sensitive"
    else:
        rating = "general"
 
    print("rating: " + rating)

    if resolution == "768x1344": 
        width = 768
        height = 1344
        aspect_ratio = "tall_wallpaper"     
    elif resolution == "896x1152": 
        width = 896
        height = 1152
        aspect_ratio = "tall"     
    elif resolution == "1024x1024": 
        width = 1024
        height = 1024
        aspect_ratio = "square"     
    elif resolution == "1152x896": 
        width = 1152
        height = 896
        aspect_ratio = "wide"     
    else:
        width = 1344
        height = 768
        aspect_ratio = "wide_wallpaper"     

    print("width: " + str(width) + ", height: " + str(height) + ", aspect_ratio: " + aspect_ratio)

    inputs = processor(
        encoder_text=prompt, 
        decoder_text=processor.decoder_tokenizer.apply_chat_template(
            {
                "aspect_ratio": aspect_ratio,
                "rating": rating,
                "length": "very_short",
                "translate_mode": "exact",
            },
           tokenize=False,
        ),
        return_tensors="pt",
    )

    with torch.inference_mode():
        outputs = model.generate(
            **inputs.to(model.device),
            do_sample=False,
            eos_token_id=processor.decoder_tokenizer.convert_tokens_to_ids(
                "</translation>"
            ),
        )
    translation = ", ".join(
        tag
        for tag in processor.batch_decode(
            outputs[0, len(inputs.input_ids[0]) :],
            skip_special_tokens=True,
        )
        if tag.strip() != ""
    )

    print("translation: " + translation)

    inputs = processor(
        encoder_text=prompt,
        decoder_text=processor.decoder_tokenizer.apply_chat_template(
            {
                "aspect_ratio": aspect_ratio,
                "rating": rating,
                "length": "long",
                "translate_mode": "approx",
                "copyright": "",
                "character": "",
                "translation": translation,
            },
            tokenize=False,
        ),
       return_tensors="pt",
    )
    with torch.inference_mode():
        outputs = model.generate(
            **inputs.to(model.device),
            do_sample=False,
            eos_token_id=processor.decoder_tokenizer.convert_tokens_to_ids("</extension>"),
        )
    extension = ", ".join(
        tag
        for tag in processor.batch_decode(
            outputs[0, len(inputs.input_ids[0]) :],
            skip_special_tokens=True,
        )
        if tag.strip() != ""
    )

    print("extension: " + extension)

    prompt =  translation + ", " + extension

    if not os.path.isdir('output'):
        os.mkdir('output')
    filename = 'output/' + datetime.now().strftime("%Y%m%d%H%M%S.png")

    print("generating as: " + filename)

    args = [SD,
        '-m', 'waiNSFWIllustrious_v140_DMD2_Q4_K.gguf', 
        '--vae-tiling',
        '-W', str(width),
        '-H', str(height),
        '--cfg-scale', "2.0",
        '--sampling-method', "lcm",
        '--steps', "8",
        '--clip-skip', "2",
        '-s', "-1",
        '--strength', "1.0",
        '-p', prompt,
        '-n', "bad quality, worst quality", 
        '-o', filename
        ]
    subprocess.run(args)
    output = Image.open(filename)
    return output

def main():
    prompt = gradio.TextArea(label = "生成したい画像を日本語の文章で入力")
    sensitive = gradio.Slider(label = "センシティブ設定", minimum = 0.0, maximum = 3.0, step = 1.0)
    resolution = gradio.Radio(["768x1344", "896x1152", "1024x1024", "1152x896", "1344x768"], label = "解像度", value = "1024x1024")

    app = gradio.Interface(fn = generate, title = "日本語画像生成", inputs = [prompt, sensitive, resolution], outputs = "image", submit_btn = "生成", clear_btn = None, flagging_mode = "never")
    app.launch(inbrowser = True)

if __name__ == "__main__":
    main()
