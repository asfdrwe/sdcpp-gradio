all: dist/sdcpp-gradio dist/sdcpp-gradio-safe

dist/sdcpp-gradio: sdcpp-gradio.py sdcpp-gradio.spec
	pyinstaller sd-gradio.spec

dist/sdcpp-gradio-safe: sdcpp-gradio-safe.py sdcpp-gradio-safe.spec
	pyinstaller sdcpp-gradio-safe.spec
