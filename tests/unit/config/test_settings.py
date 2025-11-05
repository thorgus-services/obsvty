"""Unit tests for OTLP gRPC configuration settings.

These tests follow the TDD approach with Red-Green-Refactor cycle and
AAA (Arrange-Act-Assert) pattern, ensuring the configuration model properly
loads from environment variables and validates settings correctly.
Tests cover all scenarios mentioned in the PRP for configuration validation.
"""

import os
from unittest.mock import patch

import pytest

from src.obsvty.config.settings import (
    OtlpGrpcSettings,
    get_server_endpoint,
    load_grpc_settings,
    validate_settings,
)


class TestOtlpGrpcSettings:
    """Test suite for the OtlpGrpcSettings configuration model."""

    def test_settings_load_from_environment(self):
        """Test that settings load correctly from environment variables."""
        # Arrange
        with patch.dict(
            os.environ,
            {
                "OTLP_HOST": "test-host",
                "OTLP_PORT": "1234",
                "OTLP_MAX_MESSAGE_LENGTH": "8388608",  # 8MB
                "OTLP_BUFFER_MAX_SIZE": "2000",
            },
        ):
            # Act
            settings = OtlpGrpcSettings()

            # Assert
            assert settings.host == "test-host"
            assert settings.port == 1234
            assert settings.max_message_length == 8388608
            assert settings.buffer_max_size == 2000

    def test_settings_fallback_to_defaults(self):
        """Test that settings use defaults when environment variables are missing."""
        # Arrange - ensure environment variables are not set
        with patch.dict(os.environ, {}, clear=True):
            # Act
            settings = OtlpGrpcSettings()

            # Assert
            assert settings.host == "localhost"
            assert settings.port == 4317
            assert settings.max_message_length == 4 * 1024 * 1024  # 4MB
            assert settings.buffer_max_size == 1000

    def test_port_validation_valid_values(self):
        """Test that port validation accepts valid port numbers."""
        # Test valid port numbers
        valid_ports = [1, 80, 443, 4317, 8080, 65535]

        for port in valid_ports:
            with patch.dict(os.environ, {"OTLP_PORT": str(port)}):
                settings = OtlpGrpcSettings()
                assert settings.port == port

    def test_port_validation_invalid_values(self):
        """Test that port validation rejects invalid port numbers."""
        # Test invalid port numbers
        invalid_ports = [0, -1, 65536, 100000]

        for port in invalid_ports:
            with patch.dict(os.environ, {"OTLP_PORT": str(port)}):
                with pytest.raises(
                    ValueError, match="Port must be between 1 and 65535"
                ):
                    OtlpGrpcSettings()

    def test_max_message_length_validation_positive_values(self):
        """Test that max message length validation accepts positive values."""
        positive_values = [1, 1024, 4 * 1024 * 1024]  # 1 byte, 1KB, 4MB

        for size in positive_values:
            with patch.dict(os.environ, {"OTLP_MAX_MESSAGE_LENGTH": str(size)}):
                settings = OtlpGrpcSettings()
                assert settings.max_message_length == size

    def test_max_message_length_validation_negative_values(self):
        """Test that max message length validation rejects non-positive values."""
        non_positive_values = [0, -1, -100]

        for size in non_positive_values:
            with patch.dict(os.environ, {"OTLP_MAX_MESSAGE_LENGTH": str(size)}):
                with pytest.raises(
                    ValueError, match="Max message length must be positive"
                ):
                    OtlpGrpcSettings()

    def test_buffer_max_size_validation_positive_values(self):
        """Test that buffer max size validation accepts positive values."""
        positive_values = [1, 100, 1000, 10000]

        for size in positive_values:
            with patch.dict(os.environ, {"OTLP_BUFFER_MAX_SIZE": str(size)}):
                settings = OtlpGrpcSettings()
                assert settings.buffer_max_size == size

    def test_buffer_max_size_validation_negative_values(self):
        """Test that buffer max size validation rejects non-positive values."""
        non_positive_values = [0, -1, -100]

        for size in non_positive_values:
            with patch.dict(os.environ, {"OTLP_BUFFER_MAX_SIZE": str(size)}):
                with pytest.raises(
                    ValueError, match="Buffer max size must be positive"
                ):
                    OtlpGrpcSettings()


class TestLoadGrpcSettingsFunction:
    """Test suite for the load_grpc_settings function."""

    def test_load_grpc_settings_returns_settings_instance(self):
        """Test that load_grpc_settings returns the correct settings instance."""
        # Arrange - no setup needed
        # Act
        settings = load_grpc_settings()

        # Assert
        assert isinstance(settings, OtlpGrpcSettings)
        # Verify defaults
        assert settings.host == "localhost"
        assert settings.port == 4317

    def test_load_grpc_settings_with_environment_variables(self):
        """Test that load_grpc_settings loads from environment variables."""
        # Arrange
        with patch.dict(os.environ, {"OTLP_HOST": "custom-host", "OTLP_PORT": "5555"}):
            # Act
            settings = load_grpc_settings()

            # Assert
            assert settings.host == "custom-host"
            assert settings.port == 5555


class TestValidateSettingsFunction:
    """Test suite for the validate_settings function."""

    def test_validate_settings_with_valid_settings(self):
        """Test that validate_settings returns True for valid settings."""
        # Arrange
        settings = OtlpGrpcSettings()

        # Act
        result = validate_settings(settings)

        # Assert
        assert result is True

    def test_validate_settings_with_default_settings(self):
        """Test that validate_settings returns True for default settings."""
        # Arrange
        settings = OtlpGrpcSettings(
            host="localhost",
            port=4317,
            max_message_length=4 * 1024 * 1024,
            buffer_max_size=1000,
        )

        # Act
        result = validate_settings(settings)

        # Assert
        assert result is True


class TestGetServerEndpointFunction:
    """Test suite for the get_server_endpoint function."""

    def test_get_server_endpoint_returns_correct_format(self):
        """Test that get_server_endpoint returns the correct host:port format."""
        # Arrange
        settings = OtlpGrpcSettings(host="localhost", port=4317)

        # Act
        endpoint = get_server_endpoint(settings)

        # Assert
        assert endpoint == "localhost:4317"

    def test_get_server_endpoint_with_custom_host_and_port(self):
        """Test that get_server_endpoint works with custom host and port."""
        # Arrange
        settings = OtlpGrpcSettings(host="example.com", port=8080)

        # Act
        endpoint = get_server_endpoint(settings)

        # Assert
        assert endpoint == "example.com:8080"
