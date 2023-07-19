## STAGE 0 BUILD WHL file
FROM python:3.11.4-slim-bookworm as buildImage
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
COPY --from=buildImage /work/config-example.yml /config/config.yml

COPY --from=buildImage /work/dist/auth_service*.whl /tmp
RUN pip install /tmp/auth_service*.whl && rm /tmp/*.whl

ENTRYPOINT [ "auth-service", "-c", "/config/config.yml" ]
