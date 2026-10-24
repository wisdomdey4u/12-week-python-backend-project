import json
from typing import Dict
from weather import WeatherService, OpenMeteoProvider, MockWeatherProvider, WeatherResult

def local_endpoint(query_params: Dict[str,str], use_mock: bool = False) -> str:
    """Simulates an API endpoint validating and service JSON payloads."""
    try:
        lat = float(query_params.get("lat", 0.0))
        lon = float(query_params.get("lon", 0.0))

        # Inject dynamic structural dependency
        provider = MockWeatherProvider(static_temp=18.2) if use_mock else OpenMeteoProvider()
        service = WeatherService(provider)

        # Execute service Logic
        result: WeatherResult = service(lat, lon)

        return json.dumps({"status": "success", "data": result}, indent=2)

    except (ValueError, AssertionError, RuntimeError) as err:
        return json.dumps({"status": "error", "message": str(err)}, indent=2)


if __name__ == "__main__":
    # Simulate a call arriving via an external client route
    request_params = {"lat": "52.5200", "lon": "13.4050"}

    print("--- Testing Mock Infastructure Hook ---")
    print(local_endpoint(request_params, use_mock=False))

    print("\n--- Testing Mock Infastructure Hook ---")
    print(local_endpoint(request_params, use_mock=True))