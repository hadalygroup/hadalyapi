FROM python:3.10
WORKDIR /app

# Install TA-lib

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install

RUN pip install TA-Lib

RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz

# Install Poetry & Setup app
RUN pip install poetry
COPY pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install
EXPOSE 
CMD poetry run dev