"""Unit tests for appstore_service.api_auth module."""
import time
import pytest
from unittest.mock import patch, mock_open, MagicMock
from appstore_service.api_auth import AppStoreConnectAuth


class TestAppStoreConnectAuth:
    """Test cases for AppStoreConnectAuth class."""

    @patch('appstore_service.api_auth.config')
    def test_init(self, mock_config):
        """Test AppStoreConnectAuth initialization."""
        mock_config.KEY_ID = "test_key_id"
        mock_config.ISSUER_ID = "test_issuer_id"
        mock_config.PRIVATE_KEY_PATH = "test_path.p8"
        mock_config.EXPIRATION_MINUTES = 19

        auth = AppStoreConnectAuth()

        assert auth.key_id == "test_key_id"
        assert auth.issuer_id == "test_issuer_id"
        assert auth.private_key_path == "test_path.p8"
        assert auth.expiration_minutes == 19
        assert auth.base_url == "https://api.appstoreconnect.apple.com/v1"
        assert auth._token is None
        assert auth._token_generated_time == 0

    @patch('appstore_service.api_auth.config')
    @patch('appstore_service.api_auth.jwt.encode')
    @patch('builtins.open', new_callable=mock_open, read_data="fake_private_key")
    @patch('time.time', return_value=1000000)
    def test_generate_jwt(self, mock_time, mock_file, mock_jwt_encode, mock_config):
        """Test JWT token generation."""
        mock_config.KEY_ID = "test_key_id"
        mock_config.ISSUER_ID = "test_issuer_id"
        mock_config.PRIVATE_KEY_PATH = "test_path.p8"
        mock_config.EXPIRATION_MINUTES = 19

        mock_jwt_encode.return_value = "fake_jwt_token"
        
        auth = AppStoreConnectAuth()
        auth._generate_jwt()

        # Verify JWT encode was called with correct parameters
        expected_headers = {
            "alg": "ES256",
            "kid": "test_key_id",
            "typ": "JWT"
        }
        expected_payload = {
            "iss": "test_issuer_id",
            "iat": 1000000,
            "exp": 1000000 + (19 * 60),
            "aud": "appstoreconnect-v1"
        }
        
        mock_jwt_encode.assert_called_once_with(
            expected_payload,
            "fake_private_key",
            algorithm="ES256",
            headers=expected_headers
        )
        
        assert auth._token == "fake_jwt_token"
        assert auth._token_generated_time == 1000000

    @patch('appstore_service.api_auth.config')
    def test_token_property_generates_new_token_when_none_exists(self, mock_config):
        """Test that token property generates a new token when none exists."""
        mock_config.KEY_ID = "test_key_id"
        mock_config.ISSUER_ID = "test_issuer_id"
        mock_config.PRIVATE_KEY_PATH = "test_path.p8"
        mock_config.EXPIRATION_MINUTES = 19

        auth = AppStoreConnectAuth()
        
        with patch.object(auth, '_generate_jwt') as mock_generate:
            auth._token = None
            _ = auth.token
            mock_generate.assert_called_once()

    @patch('appstore_service.api_auth.config')
    @patch('time.time')
    def test_token_property_generates_new_token_when_expired(self, mock_time, mock_config):
        """Test that token property generates a new token when current one is expired."""
        mock_config.KEY_ID = "test_key_id"
        mock_config.ISSUER_ID = "test_issuer_id"
        mock_config.PRIVATE_KEY_PATH = "test_path.p8"
        mock_config.EXPIRATION_MINUTES = 19

        auth = AppStoreConnectAuth()
        auth._token = "old_token"
        auth._token_generated_time = 1000000
        
        # Set current time to be past expiration
        mock_time.return_value = 1000000 + (19 * 60) + 1
        
        with patch.object(auth, '_generate_jwt') as mock_generate:
            _ = auth.token
            mock_generate.assert_called_once()

    @patch('appstore_service.api_auth.config')
    @patch('time.time')
    def test_token_property_returns_existing_valid_token(self, mock_time, mock_config):
        """Test that token property returns existing token when still valid."""
        mock_config.KEY_ID = "test_key_id"
        mock_config.ISSUER_ID = "test_issuer_id"
        mock_config.PRIVATE_KEY_PATH = "test_path.p8"
        mock_config.EXPIRATION_MINUTES = 19

        auth = AppStoreConnectAuth()
        auth._token = "valid_token"
        auth._token_generated_time = 1000000
        
        # Set current time to be within expiration window
        mock_time.return_value = 1000000 + (10 * 60)  # 10 minutes after generation
        
        with patch.object(auth, '_generate_jwt') as mock_generate:
            token = auth.token
            mock_generate.assert_not_called()
            assert token == "valid_token"

    @patch('appstore_service.api_auth.config')
    @patch('time.time', return_value=1000000)
    def test_headers_property(self, mock_time, mock_config):
        """Test that headers property returns correct HTTP headers."""
        mock_config.KEY_ID = "test_key_id"
        mock_config.ISSUER_ID = "test_issuer_id"
        mock_config.PRIVATE_KEY_PATH = "test_path.p8"
        mock_config.EXPIRATION_MINUTES = 19

        auth = AppStoreConnectAuth()
        
        # Set a valid token and timestamp to avoid regeneration
        auth._token = "test_token"
        auth._token_generated_time = 1000000  # Current time, so token is valid
        
        headers = auth.headers
        
        expected_headers = {
            "Authorization": "Bearer test_token",
            "Content-Type": "application/json"
        }
        
        assert headers == expected_headers