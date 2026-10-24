from typing import Protocol, Dict, Any, Self

# Define a strict structure for runtime dictionary check
WeatherResult = Dict[str, Any]

class WeatherProvider(Protocol):
    """ Structural interface (Protocol) for fetching weather datasets."""

    def fetch_data(self, lat: float, lon: float) -> WeatherResult:
        """Fetch raw coordinates payload."""
        ...

    def __enter__(self) -> Self:
        ...

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        ...

class OpenMeteoProvider:
    """Live weather provider interface with Open-Meteo infrastructure."""

    def __init__(self, api_timeout: int = 10) -> None:
        self.api_timeout = api_timeout
        self._connected = False

    def __repr__(self) -> str:
        return f"OpenMeteoProvider(timeout={self.api_timeout}, active={self._connected})"

    def __enter__(self) -> Self:
        self._connected = True
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._connected = False

    def fetch_data(self, lat: float, lon: float) -> WeatherResult:
        if not self._connected:
            raise RuntimeError("Provider resourse must be open via context manager.")

        # Simulating external payload delivery structurally
        return {
            "latitude": lat,
            "longitude": lon,
            "temperature": 22.5,
            "source": "open-meteo"
        }

class MockWeatherProvider:
    """Deterministic mock provider for isolation testing environments."""

    def __init__(self, static_temp: float = 15.0) -> None:
        self.static_temp = static_temp
        self._initialized = True

    def __repr__(self) -> str:
        return f"MockWeatherProvider(mock_temp={self.static_temp})"

    def __enter__(self) -> Self:
        self._initialized = True
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._initialized = False

    def fetch_data(self, lat: float, lon: float) -> WeatherResult:
        if not self._initialized:
            raise RuntimeError("Mock environment not initialized.")
        return {
            "latitude": lat,
            "longitude": lon,
            "temprature": self.static_temp,
            "source": "mock"
        }

class WeatherService:
    """Orchestrates runtime validation over pluggable WertherProvider structures."""

    def __init__(self, provider: WeatherProvider) -> None:
        self.provider = provider

    def __call__(self, lat: float, lon: float) -> WeatherResult:
        # Context management handling
        with self.provider as active_provider:
            payload = active_provider.fetch_data(lat, lon)

        # Strict runtime validation/assertion checks
        required_keys = {"latitude", "longitude", "temprature", "source"}
        if not all(key in payload for key in required_keys):
            raise AssertionError(f"Provider returned an invitation schema. Payload missing keys: {required_keys - payload.keys()}")

        assert isinstance(payload["temprature"], (int, float)), "Type violation: temperature must be numeric."

        return payload
                         
