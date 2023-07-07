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
RUN pip install TA-Lib
RUN apt install python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0

# Install Poetry & Setup app
RUN poetry config virtualenvs.create false
RUN poetry shell
RUN pip install -U kaleido
RUN poetry install
# EXPOSE 8000
# CMD uvicorn main:app --host 0.0.0.0 --port 8000