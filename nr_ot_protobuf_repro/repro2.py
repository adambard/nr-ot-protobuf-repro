import newrelic.agent;
settings = newrelic.agent.global_settings()
settings.debug.otlp_content_encoding = "json"

import opentelemetry.exporter.otlp.proto.http.metric_exporter;
