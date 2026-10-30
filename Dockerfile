# Reproducible Prism MCP server image.
#   docker build -t prism-mcp .
#   docker run --rm -p 8790:8790 \
#       -e PRISM_CH_HOST=http://clickhouse:8123 -e PRISM_CH_PASSWORD=... \
#       prism-mcp
# Stdio mode (for Claude Desktop/Code) instead of HTTP:
#   docker run --rm -i prism-mcp python prism_mcp.py
FROM python:3.12-slim

# fonts-dejavu-core: make_chart renders with DejaVu; without it chart
# generation fails with "cannot open resource" in a slim image.
RUN apt-get update \
    && apt-get install -y --no-install-recommends fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 10001 app

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY prism/ ./prism/
COPY prism_mcp.py README.md ./

USER app
ENV PYTHONUNBUFFERED=1 PRISM_MCP_HOST=0.0.0.0 PRISM_MCP_PORT=8790
EXPOSE 8790

ENTRYPOINT ["python", "prism_mcp.py"]
CMD ["--http", "--host", "0.0.0.0", "--port", "8790"]
