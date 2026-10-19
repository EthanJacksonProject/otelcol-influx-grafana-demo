import random
import time

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    OTLPMetricExporter,
)

INTERVAL_SECONDS = .1
JITTER = 1.5
MIN_VALUE = 0.0
MAX_VALUE = 100.0

# Initialize each gauge with its own starting value.
values = {f"lead_{i}": random.uniform(40.0, 60.0) for i in range(1, 16)}


def make_callback(name):
    def callback(options):
        return [metrics.Observation(values[name])]

    return callback


# Export collected metrics to the local OpenTelemetry Collector.
reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(
        endpoint="http://localhost:4318/v1/metrics",
    ),
    export_interval_millis=INTERVAL_SECONDS * 1000,
)

provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter("lead_generator")

# Register 15 observable gauges.
gauges = [
    meter.create_observable_gauge(
        name=name,
        description=f"Mock measurement for {name}",
        unit="1",
        callbacks=[make_callback(name)],
    )
    for name in values
]

print("Exporting 15 gauge metrics to http://localhost:4318/v1/metrics")
print("Press Ctrl+C to stop.")

try:
    while True:
        # Independently jitter each measurement.
        print("exportin")
        for name in values:
            values[name] = max(
                MIN_VALUE,
                min(MAX_VALUE, values[name] + random.uniform(-JITTER, JITTER)),
            )

        time.sleep(INTERVAL_SECONDS)

except KeyboardInterrupt:
    print("\nShutting down exporter...")

finally:
    provider.shutdown()
    print("Exporter stopped.")
