FROM quay.io/astronomer/astro-runtime:12.2.0

USER root
RUN apt update && \
    apt install -y curl  # Se você precisar de outras dependências

RUN python3 -m pip install playwright
RUN python3 -m playwright install --with-deps

# Garantir permissões
RUN chmod -R 755 /usr/local/airflow/ && \
    chmod -R 755 /usr/local/airflow/include/downloads && \
    chown -R astro:astro /usr/local/airflow/

USER astro
RUN playwright install


