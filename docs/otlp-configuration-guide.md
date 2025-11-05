# OTLP gRPC Configuration and Client Integration Guide

This document provides comprehensive information on configuring the OTLP gRPC server and connecting OTLP clients to it.

## Table of Contents
- [Server Configuration](#server-configuration)
- [Environment Variables](#environment-variables)
- [Client Integration](#client-integration)
- [Example Client](#example-client)
- [Troubleshooting](#troubleshooting)

## Server Configuration

The OTLP gRPC server is configured using environment variables following the principles of configuration as code. The server uses a `OtlpGrpcSettings` Pydantic model for validated configuration management.

### Configuration Model

The primary configuration model is `OtlpGrpcSettings` with the following fields:

- `host`: Host address for the gRPC server to bind to (default: "localhost")
- `port`: Port number for the gRPC server (default: 4317, the standard OTLP port)
- `max_message_length`: Maximum message size in bytes that the server will accept (default: 4MB)
- `buffer_max_size`: Maximum size of the trace buffer (default: 1000)

### Validation

The configuration model includes validation for:
- Port numbers (1-65535)
- Positive values for `max_message_length` and `buffer_max_size`
- Proper environment variable loading

## Environment Variables

### Standard OTLP Configuration
These are the main configuration variables following the PRP requirements:

```
# OTLP_HOST: Host address for the gRPC server (default: localhost)
OTLP_HOST=localhost

# OTLP_PORT: Port number for the gRPC server (default: 4317)
OTLP_PORT=4317

# OTLP_MAX_MESSAGE_LENGTH: Maximum message size in bytes (default: 4194304 = 4MB)
OTLP_MAX_MESSAGE_LENGTH=4194304

# OTLP_BUFFER_MAX_SIZE: Maximum size of the trace buffer (default: 1000)
OTLP_BUFFER_MAX_SIZE=1000
```

### Backward Compatibility Variables
For compatibility with existing implementations:

```
OTLP_GRPC_HOST=0.0.0.0
OTLP_GRPC_PORT=4317
OTLP_GRPC_MAX_BUFFER_SIZE=10000
OTLP_GRPC_MAX_MESSAGE_LENGTH=4194304
OTLP_GRPC_ENABLE_REFLECTION=false
OTLP_GRPC_ENABLE_LOGS_SERVICE=false
```

### Setup Instructions

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Adjust the values in `.env` as needed for your environment.

3. The server will automatically load these values when started.

## Client Integration

To connect an OTLP client to the server, configure the client with the same endpoint information used by the server.

### Python Client Example

Here's how to configure an OpenTelemetry Python client:

```python
import os
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Read configuration from environment variables
host = os.getenv("OTLP_HOST", "localhost")
port = os.getenv("OTLP_PORT", "4317")
endpoint = f"{host}:{port}"

# Create the OTLP exporter
otlp_exporter = OTLPSpanExporter(
    endpoint=endpoint,
    insecure=True,  # Set to False for TLS in production
)

# Set up the tracer provider
tracer_provider = TracerProvider()
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)
trace.set_tracer_provider(tracer_provider)

# Get a tracer
tracer = trace.get_tracer(__name__)

# Use the tracer to create spans
with tracer.start_as_current_span("example-span") as span:
    span.set_attribute("key", "value")
    print("Trace sent to OTLP server!")
```

### Other Language Clients

Most OTLP-compatible clients can be configured with the endpoint information:

- **Endpoint Format**: `host:port` (e.g., `localhost:4317`)
- **Protocol**: gRPC (insecure for development, TLS for production)
- **Headers**: None required by default (can be configured as needed)

## Example Client

The project includes a complete example client in `examples/otlp_client.py` that demonstrates:

1. Reading configuration from environment variables
2. Creating an OTLP client with the proper settings
3. Setting up tracing with the OTLP exporter
4. Sending example traces to the server

To run the example client:

```bash
# Make sure the OTLP server is running first:
python -m obsvty

# In another terminal, run the client example:
python examples/otlp_client.py
```

The example client will connect to the configured endpoint and send sample traces to demonstrate the connection.

## Troubleshooting

### Common Issues

1. **Connection Refused**: Ensure the OTLP server is running and accessible at the configured host/port.
2. **Timeout Errors**: Check that `OTLP_MAX_MESSAGE_LENGTH` is sufficient for your trace payload sizes.
3. **Environment Variables Not Loading**: Verify that your `.env` file is in the correct location and properly formatted.

### Verification Steps

1. Confirm the server is running:
   ```bash
   # Should show the server endpoint
   python -m obsvty
   ```

2. Verify environment variables are set:
   ```bash
   echo "OTLP_HOST: $OTLP_HOST"
   echo "OTLP_PORT: $OTLP_PORT"
   ```

3. Test the example client:
   ```bash
   python examples/otlp_client.py
   ```

### Logging

The server includes logging that shows configuration at startup:
- Configuration values loaded from environment
- Server endpoint information
- Connection details

Check the logs to verify the server is configured correctly.

## Architecture Compliance

This configuration implementation follows the Hexagonal Architecture principles:

- **Configuration as Code**: Settings externalized from application code
- **Dependency Inversion**: Configuration loading does not depend on infrastructure details
- **Environment-based Setup**: Flexible configuration for different deployment scenarios
- **Validation**: Proper validation ensures configuration safety
- **Separation of Concerns**: Clear configuration management module

The implementation also follows SOLID principles with proper validation, naming conventions, and architectural layering as specified in the requirements.