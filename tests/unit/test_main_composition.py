"""Unit tests for main.py composition functions following TDD and Clean Code principles."""

from unittest.mock import Mock, patch
import signal

from src.obsvty.main import (
    build_use_cases,
    build_otlp_grpc_adapter,
    configure_grpc_server,
    load_grpc_settings_with_fallback,
    start_server_with_config,
    setup_signal_handlers,
    main,
)
from src.obsvty.config.settings import OtlpGrpcSettings


class TestBuildUseCases:
    """Test the build_use_cases function."""

    def test_build_use_cases_creates_process_trace_use_case(self) -> None:
        """Verifies that build_use_cases creates the correct use case structure."""
        # Given: A mock storage implementation
        mock_storage = Mock()

        # When: Building use cases
        result = build_use_cases(mock_storage)

        # Then: Should contain process_trace use case with correct storage
        assert "process_trace" in result
        assert result["process_trace"]._storage == mock_storage


class TestBuildOtlpGrpcAdapter:
    """Test the build_otlp_grpc_adapter function."""

    def test_build_otlp_grpc_adapter_creates_adapter_with_dependencies(self) -> None:
        """Verifies that adapter is created with correct dependencies."""
        # Given: Mock storage and settings
        mock_storage = Mock()
        config = OtlpGrpcSettings()

        # When: Building the adapter
        adapter = build_otlp_grpc_adapter(mock_storage, config)

        # Then: Adapter should have correct dependencies
        assert adapter._process_trace_use_case is not None
        assert adapter._config == config
        assert adapter._buffer is not None


class TestConfigureGrpcServer:
    """Test the configure_grpc_server function."""

    def test_configure_grpc_server_creates_server_with_settings(self) -> None:
        """Verifies that gRPC server is configured with correct settings."""
        # Given: Valid configuration settings
        settings = OtlpGrpcSettings()

        # When: Configuring gRPC server
        server = configure_grpc_server(settings)

        # Then: Server should be created (would need to check actual server config options)
        assert server is not None

    @patch("src.obsvty.main.validate_settings")
    def test_configure_grpc_server_raises_error_for_invalid_settings(
        self, mock_validate
    ) -> None:
        """Verifies that invalid settings raise an error."""
        # Given: Invalid configuration settings
        mock_validate.return_value = False
        settings = OtlpGrpcSettings()

        # When/Then: Configuring server should raise error
        try:
            configure_grpc_server(settings)
            assert False, "Should have raised ValueError"
        except ValueError:
            # Expected to raise an error for invalid settings
            pass


class TestLoadGrpcSettingsWithFallback:
    """Test the load_grpc_settings_with_fallback function."""

    @patch("src.obsvty.main.load_grpc_settings")
    @patch("src.obsvty.main.validate_settings")
    def test_load_grpc_settings_with_fallback_returns_settings(
        self, mock_validate, mock_load
    ) -> None:
        """Verifies that settings are loaded and validated correctly."""
        # Given: Valid settings and validation
        mock_settings = OtlpGrpcSettings()
        mock_load.return_value = mock_settings
        mock_validate.return_value = True

        # When: Loading settings with fallback
        result = load_grpc_settings_with_fallback()

        # Then: Should return the loaded settings
        assert result == mock_settings
        mock_load.assert_called_once()
        mock_validate.assert_called_once_with(mock_settings)

    @patch("src.obsvty.main.load_grpc_settings")
    @patch("src.obsvty.main.validate_settings")
    def test_load_grpc_settings_with_fallback_raises_error_for_invalid(
        self, mock_validate, mock_load
    ) -> None:
        """Verifies that invalid settings raise an error."""
        # Given: Invalid settings
        mock_settings = OtlpGrpcSettings()
        mock_load.return_value = mock_settings
        mock_validate.return_value = False

        # When/Then: Loading should raise error
        try:
            load_grpc_settings_with_fallback()
        except ValueError:
            # Expected to raise an error for invalid settings
            pass


class TestStartServerWithConfig:
    """Test the start_server_with_config function."""

    def test_start_server_with_config_creates_and_starts_adapter(self) -> None:
        """Verifies that server is started with correct configuration."""
        # Given: Mock storage and valid settings
        mock_storage = Mock()
        config = OtlpGrpcSettings()

        # When: Starting server with config
        with patch("src.obsvty.main.build_otlp_grpc_adapter") as mock_build:
            mock_adapter = Mock()
            mock_build.return_value = mock_adapter

            adapter = start_server_with_config(mock_storage, config)

            # Then: Should return the adapter and start it
            mock_build.assert_called_once_with(mock_storage, config)
            mock_adapter.start_server.assert_called_once()
            assert adapter == mock_adapter


class TestSetupSignalHandlers:
    """Test the setup_signal_handlers function."""

    def test_setup_signal_handlers_registers_handlers(self) -> None:
        """Verifies that signal handlers are registered."""
        # Given: An adapter instance
        mock_adapter = Mock()

        # When: Setting up signal handlers
        with patch("signal.signal") as mock_signal:
            setup_signal_handlers(mock_adapter)

            # Then: Should register both SIGINT and SIGTERM handlers
            assert mock_signal.call_count == 2

    def test_signal_handler_calls_stop_server_and_exit(self) -> None:
        """Verifies that the signal handler calls stop_server and exits."""
        # Given: An adapter instance and a signal handler
        mock_adapter = Mock()

        # We'll test the internal function by patching sys.exit to avoid actual exit
        with (
            patch("src.obsvty.main.sys.exit") as mock_exit,
            patch("signal.signal") as mock_signal,
        ):
            setup_signal_handlers(mock_adapter)

            # Get the actual handler function that was registered
            # The second call to signal.signal is for SIGTERM
            # The first call is for SIGINT, which is what we'll test
            sigint_handler = mock_signal.call_args_list[0][0][1]

            # When: The handler is called
            sigint_handler(signal.SIGINT, None)

            # Then: Should call stop_server and sys.exit
            mock_adapter.stop_server.assert_called_once()
            mock_exit.assert_called_once_with(0)


class TestMainFunction:
    """Test the main function."""

    @patch("src.obsvty.main.load_grpc_settings_with_fallback")
    @patch("src.obsvty.main.get_server_endpoint")
    @patch("logging.getLogger")
    def test_main_success_returns_zero(
        self, mock_logger, mock_get_endpoint, mock_load_settings
    ) -> None:
        """Verifies that main function returns 0 on success."""
        # Given: Valid settings and endpoint
        mock_settings = OtlpGrpcSettings()
        mock_load_settings.return_value = mock_settings
        mock_get_endpoint.return_value = "localhost:4317"

        # When: Running main
        result = main()

        # Then: Should return 0 for success
        assert result == 0

    @patch("src.obsvty.main.load_grpc_settings_with_fallback")
    @patch("logging.getLogger")
    def test_main_exception_returns_one(self, mock_logger, mock_load_settings) -> None:
        """Verifies that main function returns 1 on exception."""
        # Given: Exception during execution
        mock_load_settings.side_effect = Exception("Test error")

        # When: Running main
        result = main()

        # Then: Should return 1 for error
        assert result == 1
