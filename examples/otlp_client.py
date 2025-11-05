#!/usr/bin/env python3
"""Example OTLP client demonstrating connection to the OTLP gRPC server."""

import os
import time

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.resource import ResourceAttributes


def get_otlp_client_config() -> dict:
    """Get OTLP client configuration from environment variables."""
    host = os.getenv("OTLP_HOST", "localhost")
    port = os.getenv("OTLP_PORT", "4317")
    endpoint = f"{host}:{port}"
    
    max_message_length = os.getenv("OTLP_MAX_MESSAGE_LENGTH", "4194304")  # 4MB default
    
    return {
        "endpoint": endpoint,
        "max_message_length": int(max_message_length),
        "insecure": True,  # For development, set to False for TLS in production
    }


def create_otlp_client(endpoint: str, insecure: bool = True) -> OTLPSpanExporter:
    """Create an OTLP client that can connect to the gRPC server."""
    otlp_exporter = OTLPSpanExporter(
        endpoint=endpoint,
        insecure=insecure,
    )
    
    return otlp_exporter


def setup_tracer_with_otlp(otlp_exporter: OTLPSpanExporter) -> trace.Tracer:
    """Set up a tracer with the OTLP exporter for sending traces."""
    tracer_provider = TracerProvider(
        resource=Resource.create(
            {
                ResourceAttributes.SERVICE_NAME: "otlp-client-example",
                ResourceAttributes.DEPLOYMENT_ENVIRONMENT: "development",
            }
        )
    )
    
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)
    
    trace.set_tracer_provider(tracer_provider)
    
    return trace.get_tracer(__name__)


def send_example_traces(tracer: trace.Tracer) -> None:
    """Send example traces to demonstrate client functionality."""
    print("Sending example traces to OTLP server...")
    
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
        config = get_otlp_client_config()
        print(f"Using OTLP server endpoint: {config['endpoint']}")
        print(f"Max message length: {config['max_message_length']} bytes")
        
        otlp_exporter = create_otlp_client(
            endpoint=config['endpoint'], 
            insecure=config['insecure']
        )
        print(f"OTLP client created for endpoint: {config['endpoint']}")
        
        tracer = setup_tracer_with_otlp(otlp_exporter)
        print("Tracer configured with OTLP exporter")
        
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