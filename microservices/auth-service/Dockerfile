## STAGE 0 BUILD WHL file
FROM python:3.11.4-slim-bookworm
WORKDIR /work

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get upgrade --yes
RUN apt-get install --yes --no-install-recommends python3-poetry

COPY . /work/
RUN rm -rf /work/dist

RUN poetry run python -m pytest /work/tests/
RUN poetry build

## Final container which installs the build package from STAGE 0
FROM python:3.11.4-slim-bookworm
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get upgrade --yes
RUN apt-get install --yes --no-install-recommends python3-poetry

RUN mkdir -p /config
VOLUME /config
COPY --from=0 /work/config-example.yml /config/config.yml

COPY --from=0 /work/dist/auth_service*.whl /tmp
RUN pip install /tmp/auth_service*.whl && rm /tmp/*.whl

# TODO: make auth_service install a start script that executes the below (see kiddy box on how i did it there)
ENTRYPOINT [ "/usr/local/lib/python3.11/site-packages/auth_service/main.py", "-c", "/config/config.yml" ]
