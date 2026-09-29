import sys, json, re

class CueDesktopAmbientTrigger:
    """
    Cue Desktop Ambient Context & Intent Trigger.
    Passively monitors active desktop telemetry, clipboard updates,
    and screen context to proactively surface just-in-time micro-actions.
    """
    def detect_contextual_cues(self, active_app, window_title, clipboard_text):
        cues = []

        # 1. Logistics / Tracking Code Detection
        if re.search(r"\b(?:1Z[0-9A-Z]{16}|9400\d{18}|[0-9]{12})", clipboard_text):
            cues.append({
                "type": "LOGISTICS_TRACKING",
                "confidence": 0.99,
                "summary": "Logistics tracking number detected on clipboard.",
                "action": "LOOKUP_PACKAGE_STATUS",
                "suggested_ui": "Package delivery status card"
            })

        # 2. Stacktrace / Error Exception in Code Editor
        if any(term in clipboard_text.lower() for term in ["traceback (most recent call last)", "nullpointerexception", "unhandledpromiserejection"]):
            cues.append({
                "type": "DEVELOPER_EXCEPTION",
                "confidence": 0.95,
                "summary": "Application exception traceback detected on clipboard.",
                "action": "AUTO_DIAGNOSE_STACKTRACE",
                "suggested_ui": "One-click fix proposal & test case generator"
            })

        # 3. Flight Code / Airline Booking
        if re.search(r"\b([A-Z]{2}|[A-Z]\d|\d[A-Z])\s?(\d{2,4})\b", clipboard_text) and "flight" in window_title.lower():
            cues.append({
                "type": "FLIGHT_RESERVATION",
                "confidence": 0.92,
                "summary": "Flight reservation or status query detected.",
                "action": "SYNC_FLIGHT_TO_AGENDA",
                "suggested_ui": "Add to Today AI Calendar & Traffic Alert"
            })

        # 4. Unformatted tabular or JSON dump
        if clipboard_text.strip().startswith("{") and clipboard_text.strip().endswith("}") and "
" not in clipboard_text:
            cues.append({
                "type": "RAW_JSON_PAYLOAD",
                "confidence": 0.88,
                "summary": "Minified JSON data detected.",
                "action": "PRETTIFY_AND_VALIDATE_SCHEMA",
                "suggested_ui": "Formatted viewer & schema validator"
            })

        if not cues:
            cues.append({
                "type": "PASSIVE_OBSERVATION",
                "confidence": 0.50,
                "summary": f"User engaged in {active_app}. No immediate intervention required.",
                "action": "STANDBY",
                "suggested_ui": None
            })

        return {
            "active_app": active_app,
            "window_title": window_title,
            "detected_cues": cues,
            "cue_count": len([c for c in cues if c["type"] != "PASSIVE_OBSERVATION"])
        }

    def formulate_proactive_suggestion(self, cue):
        return {
            "headline": f"💡 Cue: {cue.get('summary')}",
            "primary_action": cue.get("action"),
            "display_mode": "SUBTLE_BANNER",
            "one_click_executable": True
        }

    def run_cue_benchmark(self):
        # Scenario 1: Developer encounters error
        c1 = self.detect_contextual_cues(
            active_app="Cursor",
            window_title="server.ts - Backend API",
            clipboard_text="Traceback (most recent call last):
  File 'app.py', line 42, in <module>
    KeyError: 'user_session_id'"
        )

        # Scenario 2: Logistics tracking code
        c2 = self.detect_contextual_cues(
            active_app="Slack",
            window_title="#general - Company Team",
            clipboard_text="Hey can you check this FedEx package: 1Z9999999999999999"
        )

        return {
            "suite": "Cue Desktop Ambient Context Trigger Benchmark",
            "developer_error_cue": c1,
            "logistics_tracking_cue": c2,
            "sample_suggestion": self.formulate_proactive_suggestion(c1["detected_cues"][0]),
            "ambient_listener_state": "PROACTIVE_MONITORING_ACTIVE"
        }
