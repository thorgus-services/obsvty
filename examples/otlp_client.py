#!/usr/bin/env python3
"""Example OTLP client demonstrating connection to the OTLP gRPC server.

This script demonstrates how to connect an OTLP client to the OTLP gRPC server
using the configuration settings, following the principles of proper client
integration and environment-based configuration management.
"""

import os
import time

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.resource import ResourceAttributes


def get_otlp_client_config() -> dict:
    """Get OTLP client configuration from environment variables.
    
    This function reads configuration from environment variables that match
    the server configuration, enabling clients to connect using the same
    configuration approach as the server.
    
    Returns:
        dict: Configuration dictionary with endpoint and connection settings
    """
    # Get configuration from environment variables
    host = os.getenv("OTLP_HOST", "localhost")
    port = os.getenv("OTLP_PORT", "4317")
    endpoint = f"{host}:{port}"
    
    # Get other configuration values
    max_message_length = os.getenv("OTLP_MAX_MESSAGE_LENGTH", "4194304")  # 4MB default
    
    return {
        "endpoint": endpoint,
        "max_message_length": int(max_message_length),
        "insecure": True,  # For development, set to False for TLS in production
    }


def create_otlp_client(endpoint: str, insecure: bool = True) -> OTLPSpanExporter:
    """Create an OTLP client that can connect to the gRPC server.
    
    Args:
        endpoint: The server endpoint in host:port format
        insecure: Whether to use insecure connection (True for development)
        
    Returns:
        OTLPSpanExporter: Configured OTLP client for trace export
    """
    # Configure the OTLP exporter with the provided endpoint
    otlp_exporter = OTLPSpanExporter(
        endpoint=endpoint,
        insecure=insecure,
        # Additional options can be configured here
    )
    
    return otlp_exporter


def setup_tracer_with_otlp(otlp_exporter: OTLPSpanExporter) -> trace.Tracer:
    """Set up a tracer with the OTLP exporter for sending traces.
    
    Args:
        otlp_exporter: The configured OTLP span exporter
        
    Returns:
        trace.Tracer: A tracer configured to export to the OTLP server
    """
    # Set up the tracer provider with resource information
    tracer_provider = TracerProvider(
        resource=Resource.create(
            {
                ResourceAttributes.SERVICE_NAME: "otlp-client-example",
                ResourceAttributes.DEPLOYMENT_ENVIRONMENT: "development",
            }
        )
    )
    
    # Add the OTLP span processor to the tracer provider
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)
    
    # Set the global tracer provider
    trace.set_tracer_provider(tracer_provider)
    
    # Get and return a tracer instance
    return trace.get_tracer(__name__)


def send_example_traces(tracer: trace.Tracer) -> None:
    """Send example traces to demonstrate client functionality.
    
    Args:
        tracer: The configured tracer to create and send traces
    """
    print("Sending example traces to OTLP server...")
    
    # Create a few example spans to send
    with tracer.start_as_current_span("example-operation-1") as span1:
        span1.set_attribute("example.key", "value1")
        span1.add_event("Example event in operation 1")
        
        time.sleep(0.1)  # Simulate some work
        
        with tracer.start_as_current_span("nested-operation") as span2:
            span2.set_attribute("nested.key", "value2")
            span2.add_event("Example event in nested operation")
            
            time.sleep(0.05)  # Simulate more work
    
    with tracer.start_as_current_span("example-operation-2") as span3:
        span3.set_attribute("example.key", "value2")
        span3.add_event("Example event in operation 2")
        
        time.sleep(0.08)  # Simulate some work


def main():
    """Main function to demonstrate OTLP client connection."""
    print("OTLP Client Example")
    print("=" * 30)
    
    try:
        # Get configuration from environment variables
        config = get_otlp_client_config()
        print(f"Using OTLP server endpoint: {config['endpoint']}")
        print(f"Max message length: {config['max_message_length']} bytes")
        
        # Create the OTLP client
        otlp_exporter = create_otlp_client(
            endpoint=config['endpoint'], 
            insecure=config['insecure']
        )
        print(f"OTLP client created for endpoint: {config['endpoint']}")
        
        # Set up the tracer with the OTLP exporter
        tracer = setup_tracer_with_otlp(otlp_exporter)
        print("Tracer configured with OTLP exporter")
        
        # Send example traces
        send_example_traces(tracer)
        print("Example traces sent successfully!")
        
        print("\nConfiguration Summary:")
        print(f"  - Endpoint: {config['endpoint']}")
        print(f"  - Connection: {'Insecure (HTTP)' if config['insecure'] else 'Secure (HTTPS)'}")
        print(f"  - Max message length: {config['max_message_length']} bytes")
        
        print("\nTo connect your own application, ensure environment variables are set:")
        print("  - OTLP_HOST: The host of your OTLP server (default: localhost)")
        print("  - OTLP_PORT: The port of your OTLP server (default: 4317)")
        print("  - OTLP_MAX_MESSAGE_LENGTH: Max message size in bytes (default: 4194304)")
        
    except Exception as e:
        print(f"Error in OTLP client example: {e}")
        print("Make sure the OTLP gRPC server is running before connecting.")
        return 1
    
    print("\nOTLP client example completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())