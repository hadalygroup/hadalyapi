FROM python:3.10
WORKDIR /app
COPY . .

RUN pip install poetry
# Install TA-lib

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install

RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz
RUN cd ..
RUN poetry shell
RUN pip install TA-Lib
# Install Poetry & Setup app
RUN poetry config virtualenvs.create false
RUN poetry install
RUN poetry shell
