FROM alpine:latest
MAINTAINER Kemad Zhong <kemadz@gmail.com>

RUN mkdir -p ~/.pip && \
echo -e "[global]\nindex-url = https://pypi.mirrors.ustc.edu.cn/simple" >~/.pip/pip.conf && \
sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
apk add --no-cache tesseract-ocr tesseract-ocr-data-equ python3 py3-pillow py3-requests && \
pip3 --no-cache-dir install pytesseract

ADD v2ex.py /

CMD ["python3", "v2ex.py"]
