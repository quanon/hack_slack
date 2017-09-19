FROM python:3.6.2

RUN apt-get update \
 && apt-get install -y \
      git \
      unzip \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/share/fonts
ADD https://github.com/mzyy94/RictyDiminished-for-Powerline/archive/3.2.4-powerline-early-2016.zip .
RUN unzip -jo 3.2.4-powerline-early-2016.zip \
 && fc-cache -fv

RUN mkdir -p /root/.matplotlibrc \
 && echo "backend : Agg" >> /root/.matplotlibrc/matplotlibrc \
 && echo "font.family : Ricty Diminished" >> /root/.matplotlibrc/matplotlibrc

WORKDIR /opt
RUN git clone https://github.com/quanon/hack_slack.git

WORKDIR /opt/hack_slack
RUN pip install -r requirements.txt
COPY config.json .
