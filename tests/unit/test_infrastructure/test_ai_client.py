import unittest
from unittest.mock import patch, Mock, MagicMock
import json
import requests

from src.debate_simulator.infrastructure.ai_client import (
    OpenAIClient, MockAIClient, AIClientError, 
    create_ai_client, validate_api_key, test_ai_connection
)


class TestOpenAIClient(unittest.TestCase):
    """Test cases for OpenAIClient."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "sk-test_key_1234567890abcdef"
        self.client = OpenAIClient(api_key=self.api_key)
    
    def test_initialization(self):
        """Test client initialization."""
        self.assertEqual(self.client.api_key, self.api_key)
        self.assertEqual(self.client.model, "gpt-4o")
        self.assertEqual(self.client.base_url, "https://api.openai.com/v1/chat/completions")
    
    def test_initialization_with_custom_model(self):
        """Test client initialization with custom model."""
        client = OpenAIClient(api_key=self.api_key, model="gpt-3.5-turbo")
        self.assertEqual(client.model, "gpt-3.5-turbo")
    
    def test_initialization_without_api_key(self):
        """Test client initialization without API key raises error."""
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(ValueError) as context:
                OpenAIClient()
            self.assertIn("OpenAI API key is required", str(context.exception))
    
    @patch('src.debate_simulator.infrastructure.ai_client.requests.post')
    def test_generate_response_success(self, mock_post):
        """Test successful response generation."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response"}}]
        }
        mock_post.return_value = mock_response
        
        messages = [{"role": "user", "content": "Test message"}]
        response = self.client.generate_response(messages)
        
        self.assertEqual(response, "Test response")
        mock_post.assert_called_once()
        
        # Check the request parameters
        call_args = mock_post.call_args
        self.assertIn('headers', call_args.kwargs)
        self.assertIn('json', call_args.kwargs)
        self.assertEqual(call_args.kwargs['headers']['Authorization'], f"Bearer {self.api_key}")
    
    @patch('src.debate_simulator.infrastructure.ai_client.requests.post')
    def test_generate_response_http_error(self, mock_post):
        """Test response generation with HTTP error."""
        # Mock HTTP error response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response
        
        messages = [{"role": "user", "content": "Test message"}]
        response = self.client.generate_response(messages)
        
        self.assertIn("Error: HTTP 401", response)
        self.assertIn("Unauthorized", response)
    
    @patch('src.debate_simulator.infrastructure.ai_client.requests.post')
    def test_generate_response_network_error(self, mock_post):
        """Test response generation with network error."""
        # Mock network error
        mock_post.side_effect = requests.exceptions.RequestException("Network error")
        
        messages = [{"role": "user", "content": "Test message"}]
        response = self.client.generate_response(messages)
        
        self.assertIn("Error generating response", response)
        self.assertIn("Network error", response)
    
    @patch('src.debate_simulator.infrastructure.ai_client.requests.post')
    def test_generate_judge_response_success(self, mock_post):
        """Test successful judge response generation."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": '{"participant": {"anger": 5, "patience": -2}}'}}]
        }
        mock_post.return_value = mock_response
        
        prompt = "Judge this debate round"
        response = self.client.generate_judge_response(prompt)
        
        self.assertIn("participant", response)
        mock_post.assert_called_once()
    
    @patch('src.debate_simulator.infrastructure.ai_client.requests.post')
    def test_generate_judge_response_error(self, mock_post):
        """Test judge response generation with error."""
        # Mock error response
        mock_post.side_effect = requests.exceptions.RequestException("Error")
        
        prompt = "Judge this debate round"
        response = self.client.generate_judge_response(prompt)
        
        self.assertEqual(response, "{}")  # Should return empty JSON on error


class TestMockAIClient(unittest.TestCase):
    """Test cases for MockAIClient."""
    
    def test_initialization_with_defaults(self):
        """Test mock client initialization with defaults."""
        client = MockAIClient()
        self.assertIsNone(client.fixed_response)
        self.assertIsNone(client.fixed_judge_response)
        self.assertEqual(client.call_count, 0)
        self.assertEqual(client.judge_call_count, 0)
    
    def test_initialization_with_fixed_responses(self):
        """Test mock client initialization with fixed responses."""
        client = MockAIClient(
            fixed_response="Fixed response",
            fixed_judge_response='{"test": "judge"}'
        )
        self.assertEqual(client.fixed_response, "Fixed response")
        self.assertEqual(client.fixed_judge_response, '{"test": "judge"}')
    
    def test_generate_response_with_fixed_response(self):
        """Test response generation with fixed response."""
        client = MockAIClient(fixed_response="Fixed test response")
        messages = [{"role": "user", "content": "Test"}]
        
        response = client.generate_response(messages)
        self.assertEqual(response, "Fixed test response")
        self.assertEqual(client.call_count, 1)
    
    def test_generate_response_without_fixed_response(self):
        """Test response generation without fixed response."""
        client = MockAIClient()
        messages = [
            {"role": "system", "content": "You are Test Character, a test role."},
            {"role": "user", "content": "Hello world"}
        ]
        
        response = client.generate_response(messages)
        
        self.assertIn("Mock response from Test Character", response)
        self.assertIn("call #1", response)
        self.assertIn("Hello world", response)
        self.assertEqual(client.call_count, 1)
    
    def test_generate_judge_response_with_fixed_response(self):
        """Test judge response generation with fixed response."""
        fixed_judge = '{"char1": {"anger": 2, "patience": -1, "uniqueness": 1}}'
        client = MockAIClient(fixed_judge_response=fixed_judge)
        
        response = client.generate_judge_response("Judge prompt")
        self.assertEqual(response, fixed_judge)
        self.assertEqual(client.judge_call_count, 1)
    
    def test_generate_judge_response_without_fixed_response(self):
        """Test judge response generation without fixed response."""
        client = MockAIClient()
        
        response = client.generate_judge_response("Judge prompt")
        
        # Should return valid JSON
        json_response = json.loads(response)
        self.assertIn("Character 1", json_response)
        self.assertIn("Character 2", json_response)
        self.assertEqual(client.judge_call_count, 1)
    
    def test_call_count_increment(self):
        """Test that call counts increment properly."""
        client = MockAIClient()
        
        # Generate multiple responses
        client.generate_response([{"role": "user", "content": "test1"}])
        client.generate_response([{"role": "user", "content": "test2"}])
        client.generate_judge_response("judge1")
        
        self.assertEqual(client.call_count, 2)
        self.assertEqual(client.judge_call_count, 1)


class TestFactoryFunctions(unittest.TestCase):
    """Test cases for factory functions."""
    
    def test_create_openai_client(self):
        """Test creating OpenAI client via factory."""
        client = create_ai_client("openai", api_key="sk-test123")
        self.assertIsInstance(client, OpenAIClient)
        self.assertEqual(client.api_key, "sk-test123")
    
    def test_create_openai_client_with_custom_model(self):
        """Test creating OpenAI client with custom model."""
        client = create_ai_client("openai", api_key="sk-test123", model="gpt-3.5-turbo")
        self.assertIsInstance(client, OpenAIClient)
        self.assertEqual(client.model, "gpt-3.5-turbo")
    
    def test_create_mock_client(self):
        """Test creating mock client via factory."""
        client = create_ai_client("mock")
        self.assertIsInstance(client, MockAIClient)
    
    def test_create_mock_client_with_fixed_responses(self):
        """Test creating mock client with fixed responses."""
        client = create_ai_client(
            "mock", 
            fixed_response="Test", 
            fixed_judge_response='{"test": "data"}'
        )
        self.assertIsInstance(client, MockAIClient)
        self.assertEqual(client.fixed_response, "Test")
    
    def test_create_unknown_client_type(self):
        """Test creating unknown client type raises error."""
        with self.assertRaises(ValueError) as context:
            create_ai_client("unknown_type")
        self.assertIn("Unknown AI client type", str(context.exception))


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_validate_api_key_valid(self):
        """Test API key validation with valid key."""
        valid_keys = [
            "sk-1234567890abcdefghijklmnop",
            "sk-very_long_api_key_that_should_be_valid",
            "sk-short_but_valid_key_123"
        ]
        
        for key in valid_keys:
            with self.subTest(key=key):
                self.assertTrue(validate_api_key(key))
    
    def test_validate_api_key_invalid(self):
        """Test API key validation with invalid keys."""
        invalid_keys = [
            "",
            None,
            "invalid_key",
            "sk-short",
            "not_starting_with_sk",
            "sk-",  # Too short
        ]
        
        for key in invalid_keys:
            with self.subTest(key=key):
                self.assertFalse(validate_api_key(key))
    
    def test_test_ai_connection_success(self):
        """Test AI connection test with successful client."""
        client = MockAIClient(fixed_response="Hello test")
        result = test_ai_connection(client)
        self.assertTrue(result)
    
    def test_test_ai_connection_error_response(self):
        """Test AI connection test with error response."""
        client = MockAIClient(fixed_response="Error: connection failed")
        result = test_ai_connection(client)
        self.assertFalse(result)
    
    def test_test_ai_connection_exception(self):
        """Test AI connection test with exception."""
        client = MockAIClient()
        
        # Mock the generate_response to raise an exception
        def raise_exception(*args, **kwargs):
            raise Exception("Connection failed")
        
        client.generate_response = raise_exception
        
        result = test_ai_connection(client)
        self.assertFalse(result)
    
    def test_test_ai_connection_empty_response(self):
        """Test AI connection test with empty response."""
        client = MockAIClient(fixed_response="")
        result = test_ai_connection(client)
        self.assertFalse(result)


class TestAIClientIntegration(unittest.TestCase):
    """Integration test cases for AI client functionality."""
    
    def test_openai_client_request_format(self):
        """Test that OpenAI client formats requests correctly."""
        with patch('src.debate_simulator.infrastructure.ai_client.requests.post') as mock_post:
            # Mock successful response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "choices": [{"message": {"content": "Response"}}]
            }
            mock_post.return_value = mock_response
            
            client = OpenAIClient(api_key="sk-test123")
            messages = [
                {"role": "system", "content": "System message"},
                {"role": "user", "content": "User message"}
            ]
            
            client.generate_response(messages)
            
            # Verify the request was made correctly
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            
            # Check URL
            self.assertEqual(call_args[0][0], "https://api.openai.com/v1/chat/completions")
            
            # Check headers
            headers = call_args.kwargs['headers']
            self.assertEqual(headers['Authorization'], "Bearer sk-test123")
            self.assertEqual(headers['Content-Type'], "application/json")
            
            # Check request data
            data = call_args.kwargs['json']
            self.assertEqual(data['model'], "gpt-4o")
            self.assertEqual(data['messages'], messages)
            self.assertEqual(data['max_tokens'], 100)
            self.assertEqual(data['temperature'], 0.8)
    
    def test_mock_client_character_name_extraction(self):
        """Test that mock client extracts character names correctly."""
        client = MockAIClient()
        
        messages = [
            {
                "role": "system", 
                "content": "You are Democratic Senator, a progressive politician.\nPersonality: Liberal views..."
            },
            {"role": "user", "content": "What do you think?"}
        ]
        
        response = client.generate_response(messages)
        
        self.assertIn("Democratic Senator", response)
        self.assertIn("call #1", response)


if __name__ == "__main__":
    unittest.main()