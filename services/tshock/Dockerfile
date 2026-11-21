FROM mcr.microsoft.com/dotnet/runtime:9.0.23-bookworm-slim@sha256:aa21f09894760dc31b207e29256fcf9a74fb14da4384b81ba49b1f038604087f
ARG TSHOCK_VERSION=6.2.1
ARG TSHOCK_SHA256=deb9189acbdbd2ee0f0a06fffe15358033859a4ba842b22f79a84bda68600105
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl unzip python3 && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /opt/tshock /app /data \
    && curl --fail --location --retry 5 --retry-all-errors "https://github.com/Pryaxis/TShock/releases/download/v${TSHOCK_VERSION}/TShock-${TSHOCK_VERSION}-for-Terraria-1.4.5.8-linux-x64-Release.zip" -o /tmp/tshock.zip \
    && echo "${TSHOCK_SHA256}  /tmp/tshock.zip" | sha256sum -c - \
    && unzip -q /tmp/tshock.zip -d /tmp/tshock-release \
    && tar xf /tmp/tshock-release/TShock-Beta-linux-x64-Release.tar -C /opt/tshock \
    && chmod 0755 /opt/tshock/TShock.Server \
    && rm -rf /tmp/tshock.zip /tmp/tshock-release \
    && useradd --uid 10001 --home-dir /data --shell /usr/sbin/nologin tshock \
    && chown -R 10001:10001 /data /opt/tshock \
    && ln -s /data/tshock/ServerLog.txt /opt/tshock/ServerLog.txt
COPY bootstrap.py /app/bootstrap.py
ENV HOME=/data PYTHONUNBUFFERED=1 PORT=8080 DOTNET_EnableDiagnostics=0
WORKDIR /opt/tshock
EXPOSE 7777 8080
STOPSIGNAL SIGTERM
ENTRYPOINT ["python3", "/app/bootstrap.py"]
