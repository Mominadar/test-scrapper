# define base image as python slim-buster.
FROM --platform=linux/amd64 python:3.10 as base

## start builder stage.

# this is the first stage of the build.
# it will install all requirements.
FROM base as builder

# install all packages for chromedriver: https://gist.github.com/varyonic/dea40abcf3dd891d204ef235c6e8dd79
RUN apt-get update
RUN apt-get install -y xvfb gnupg wget curl unzip --no-install-recommends
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list 

RUN apt-get update -qqy --no-install-recommends 
RUN apt-get install -y google-chrome-stable

RUN echo $(google-chrome -product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*")
RUN wget -q --continue -P /chromedriver "https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chromedriver-linux64.zip"
RUN echo $(ls chromedriver/)

RUN unzip /chromedriver/chromedriver-linux64.zip -d /chromedriver

COPY . /app

# make the chromedriver executable and move it to default selenium path.
RUN chmod +x /chromedriver/chromedriver-linux64
RUN cp -r /chromedriver/chromedriver-linux64 /app/chromedriver

RUN mv /chromedriver/chromedriver-linux64 /usr/bin/chromedriver

# copy any python requirements file into the install directory and install all python requirements.
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# RUN pip install --upgrade --no-cache-dir -r /requirements.txt
RUN rm /requirements.txt # remove requirements file from container.

RUN pip install selenium==3.141.0 
RUN pip install --upgrade urllib3==1.26.16
# copy the source code into /app and move into that directory.

# this is the image this is run.
FROM builder

# set the proxy addresses
ENV HTTP_PROXY "http://134.209.29.120:8080"
ENV HTTPS_PROXY "https://45.77.71.140:9050"

RUN apt-get install -y vim
RUN apt-get install -y xvfb
RUN apt-get -y install xorg xvfb gtk2-engines-pixbuf
RUN apt-get -y install dbus-x11 xfonts-base xfonts-100dpi xfonts-75dpi xfonts-scalable
RUN export DISPLAY=:99


ENV DBUS_SESSION_BUS_ADDRESS autolaunch:

# RUN sysctl -w kernel.unprivileged_userns_clone=1
RUN apt-get install -y dbus
RUN dbus-daemon --system

ENV CHROME_DEVEL_SANDBOX /usr/bin/chrome-devel-sandbox

RUN Xvfb -ac :99 -screen 0 1280x1024x16 &

WORKDIR /app

# default entry point.
CMD ["python", "webscraper.py", "-c"]
## end base stage.