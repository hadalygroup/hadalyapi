# Define custom function directory
ARG FUNCTION_DIR="/function"

FROM python:3.10 as build-image
# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Create the function directory and copying the code
RUN mkdir -p ${FUNCTION_DIR}
COPY . ${FUNCTION_DIR}

# Cd into the function directory
RUN cd ${FUNCTION_DIR}
# Installing poetry
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


# Needed for Weasyprint
RUN apt install libpango-1.0-0 libpangoft2-1.0-0

# Install Poetry & Setup app
RUN poetry config virtualenvs.create false

#For plotly
RUN pip install -U kaleido

# Install dependencies
RUN poetry shell
RUN poetry install
# Command to run the FastAPI application with Uvicorn
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# CD out of function directory
RUN cd ..

FROM python:3.10-slim
# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}
# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# Pass the name of the function handler as an argument to the runtime
CMD [ "main.handler" ]
