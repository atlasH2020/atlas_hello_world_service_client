FROM python:3.7-slim

COPY . /usr/src/app
WORKDIR /usr/src/app

#COPY requirements.txt ./

#COPY main.py ./
#COPY config.py ./
#COPY hello_world_service_consumer.py ./
#COPY service_client service_client
#COPY registry_client registry_client
#COPY atlas_service_client atlas_service_client
#COPY routers routers
#COPY static static
#COPY templates templates
#COPY user_management user_management

#RUN pip install --upgrade pip
#RUN pip install --upgrade pip setuptools==44.1.0

RUN apt-get -y update
RUN apt-get -y install git
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e git+https://github.com/atlasH2020/atlas_registry_client.git#egg=registry_client
RUN pip install -e git+https://github.com/atlasH2020/atlas_service_client.git#egg=service_client
#RUN pip install /usr/src/app/registry_client
#RUN pip install /usr/src/app/service_client

ENTRYPOINT ["python", "./main.py"]