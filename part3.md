# 9. System Architecture

## 9.1 Layered Architectural Overview
SafeHer adopts a modular, three-tier architecture designed for scalability, maintainability, and real-time responsiveness. The system is partitioned into three logical layers: **Presentation (Frontend)**, **Application & Data (Backend)**, and **Intelligence (AI)**. This separation enables independent evolution of components while ensuring secure, low-latency communication.

```
┌─────────────────────────────────────┐
│         PRESENTATION LAYER          │
│  • Flutter Mobile Application       │
│  • Sensor Integration (GPS, IMU)    │
│  • Local State Management           │
│  • Offline Persistence (Hive/SQLite)│
└────────────┬────────────────────────┘
             │ HTTPS / gRPC
             ▼
┌─────────────────────────────────────┐
│      APPLICATION & DATA LAYER       │
│  • Firebase Authentication          │
│  • Cloud Firestore (NoSQL DB)       │
│  • Cloud Functions (Serverless)     │
│  • Firebase Cloud Messaging (FCM)   │
│  • Crashlytics & Performance Monitor│
└────────────┬────────────────────────┘
             │ Secure API Proxy
             ▼
┌─────────────────────────────────────┐
│         INTELLIGENCE LAYER          │
│  • Google Gemini Pro API            │
│  • Prompt Engineering & Context     │
│  • Risk Score Normalization         │
│  • Fallback Rule Engine             │
└─────────────────────────────────────┘
```

`[Figure 2: Three-Tier System Architecture Diagram – to be inserted]`  
*Caption: Data flows from mobile sensors through Firebase backend services to Google Gemini for AI inference, with autonomous alerting routed back via FCM to trusted contacts.*

## 9.2 Component Interactions

### 9.2.1 Frontend ↔ Backend Communication
- **Authentication**: Phone OTP via Firebase Auth; JWT tokens attached to all subsequent requests.
- **Data Sync**: Bi-directional Firestore listeners for real-time location/alert updates; offline-first design with local queue for pending writes.
- **Event Triggers**: Cloud Functions invoked via HTTPS calls for danger score computation and alert dispatch.

### 9.2.2 Backend ↔ AI Layer Communication
- **Secure Proxy Pattern**: Gemini API calls are routed through authenticated Cloud Functions to prevent client-side key exposure.
- **Request Batching**: Context vectors from multiple users are batched (where privacy-compliant) to optimize API quota usage.
- **Response Validation**: AI outputs are parsed, validated against schema, and normalized before score integration.

### 9.2.3 Alert Distribution Pipeline
```
Danger Score ≥ Threshold 
→ Cloud Function: validate_user_preferences() 
→ Construct alert_payload {user_id, location, risk_score, timestamp} 
→ Parallel dispatch: 
   • FCM to trusted contacts' devices 
   • SMS fallback via Twilio (if enabled) 
   • Log to Firestore:alerts collection
→ Initiate live_location_stream (15-min TTL)
```

## 9.3 Security & Privacy Architecture
- **Data Minimization**: Only essential features (e.g., location accuracy radius, not raw coordinates) are transmitted for AI processing.
- **Encryption**: Data in transit (TLS 1.3); data at rest (Firestore server-side encryption); optional end-to-end encryption for alert payloads.
- **Access Control**: Firestore Security Rules enforce user-level document ownership; Cloud Functions verify caller identity via Firebase Admin SDK.
- **Auditability**: All critical operations (score computation, alert triggers) are logged with immutable timestamps for forensic review.

---

# 10. Methodology

## 10.1 End-to-End Workflow
SafeHer operates on a continuous, event-driven loop. The methodology follows five sequential phases:

```
[Phase 1] Data Acquisition → [Phase 2] Preprocessing → [Phase 3] Risk Scoring 
→ [Phase 4] Decision & Alerting → [Phase 5] Feedback & Logging
```

## 10.2 Phase 1: Contextual Data Collection
The Flutter client collects sensor data at adaptive intervals based on motion state:

| Sensor | Sampling Rate | Purpose | Preprocessing |
|--------|--------------|---------|--------------|
| GPS | 30s (stationary) → 5s (moving) | Location, speed, route deviation | Kalman filter, accuracy validation |
| Accelerometer | 10Hz (burst on anomaly) | Fall detection, sudden stops | Low-pass filter, magnitude calculation |
| Gyroscope | 5Hz | Orientation changes, vehicle detection | Sensor fusion with accelerometer |
| System Clock | Event-triggered | Time-of-day, duration analysis | UTC normalization |
| Network Info | On change | Connectivity risk factor | Signal strength (dBm) classification |

*Adaptive sampling reduces battery drain by 40–60% compared to fixed-rate polling [11].*

## 10.3 Phase 2: Feature Engineering & Rule-Based Pre-Filtering
Raw sensor data is transformed into contextual features:

```python
# Pseudocode: Feature Extraction
def extract_features(sensor_stream):
    features = {
        'time_risk': calculate_time_risk(timestamp),  # 0-10: night=high
        'location_type': classify_location(lat, lng),  # commercial/residential/isolated
        'isolation_index': compute_isolation(lat, lng, radius=200m),  # POI density
        'velocity_variance': std_dev(speed_window_last_2min),
        'route_deviation': haversine_deviation(planned_route, actual_path),
        'motion_anomaly': detect_abrupt_stop(accel_data),
        'network_risk': 1 if signal_strength < -100dBm else 0
    }
    return features
```

**Rule-Based Risk Aggregation (Edge)**:
```
Base_Risk = 0
IF time_risk ≥ 7 → Base_Risk += 15
IF location_type == "isolated" → Base_Risk += 20
IF velocity_variance > threshold AND motion_anomaly → Base_Risk += 25
IF route_deviation > 200m AND isolation_index > 0.8 → Base_Risk += 15
IF network_risk == 1 → Base_Risk += 10
Base_Risk = min(Base_Risk, 50)  # Cap at 50 for hybrid balance
```

## 10.4 Phase 3: Hybrid Danger Score Computation
The Verified Safety Matrix fuses rule-based and AI scores:

```
Final_Danger_Score = α·Base_Risk + β·AI_Risk_Score
Where:
  α = 0.5, β = 0.5 (calibrated via validation set)
  AI_Risk_Score ∈ [0, 50] (normalized from Gemini output)
```

*Threshold calibration*: Default alert threshold = 60; tunable via Firebase Remote Config per region/user preference.

## 10.5 Phase 4: Autonomous Decision & Alerting
```python
# Pseudocode: Alert Trigger Logic
def evaluate_and_alert(user_id, danger_score, context):
    if danger_score >= get_user_threshold(user_id):
        # Validate user is not manually paused
        if not is_monitoring_paused(user_id):
            alert_payload = {
                'user_id': user_id,
                'timestamp': iso_now(),
                'location': get_last_known_location(user_id),
                'risk_score': danger_score,
                'context_summary': generate_context_summary(context),
                'alert_id': uuid_v4()
            }
            # Dispatch via Cloud Function
            trigger_cloud_function('dispatch_alert', alert_payload)
            # Start live location stream (15-min TTL)
            initiate_location_stream(user_id, duration_minutes=15)
            # Log for audit
            log_to_firestore('alerts', alert_payload)
```

## 10.6 Phase 5: Feedback Loop & Continuous Improvement
- **User Feedback**: Post-alert, trusted contacts can mark "False Alarm" or "Confirmed Threat" via app UI.
- **Model Retraining**: Anonymized feedback + context vectors are aggregated weekly to refine rule weights and AI prompt examples.
- **A/B Testing**: Thresholds and rule parameters are tested across user cohorts to optimize precision/recall trade-offs.

---

# 11. Modules Description

## 11.1 Authentication Module
- **Responsibility**: Secure user onboarding and session management.
- **Implementation**: Firebase Authentication with phone OTP; custom claims for role-based access (user/admin).
- **Security**: Token refresh, automatic logout on suspicious activity, biometric re-auth for sensitive actions.

## 11.2 Location Tracking Module
- **Responsibility**: Continuous, privacy-aware geospatial monitoring.
- **Implementation**: 
  - `geolocator` Flutter plugin with background execution permissions.
  - Adaptive polling: 30s (stationary) → 5s (moving) → 1s (high-risk detected).
  - Local caching with Firestore sync; offline queue for pending updates.
- **Privacy**: Location accuracy fuzzing (±50m) for non-emergency analytics; user-controlled sharing granularity.

## 11.3 Motion Analysis Module
- **Responsibility**: Detect behavioral anomalies indicative of distress.
- **Implementation**:
  - Accelerometer burst sampling on sudden deceleration (>3m/s² change).
  - Step-count deviation analysis (e.g., running pattern vs. walking baseline).
  - Vehicle detection via gyroscope + speed correlation.
- **Output**: Binary flags (`abrupt_stop`, `unusual_motion`) fed to rule engine.

## 11.4 Danger Scoring Module (Verified Safety Matrix)
- **Responsibility**: Compute dynamic risk score via hybrid logic.
- **Subcomponents**:
  - `RuleEngine`: Edge-based Dart implementation of risk heuristics.
  - `AIProxy`: Secure Cloud Function wrapper for Gemini API calls.
  - `ScoreNormalizer`: Combines and scales outputs to 0–100 range.
- **Fallback**: If AI service unavailable, system defaults to rule-based score with conservative threshold (50).

## 11.5 Alert Distribution Module
- **Responsibility**: Reliable, multi-channel emergency notification.
- **Implementation**:
  - Primary: Firebase Cloud Messaging with high-priority flags.
  - Fallback: Twilio SMS API (user-opt-in) with templated messages.
  - Retry logic: Exponential backoff (1s, 2s, 4s) for failed deliveries.
- **Payload**: Includes location link (Google Maps), risk score, timestamp, and one-tap "I'm Safe" acknowledgment.

## 11.6 Fear Map Module (Community Safety Layer)
- **Responsibility**: Aggregate anonymized risk data to visualize area-level safety trends.
- **Implementation**:
  - Differential privacy: Add Laplace noise to location clusters before aggregation.
  - Heatmap generation: Kernel density estimation on Firestore `dangerScores` collection.
  - Client-side rendering: Flutter `google_maps_flutter` with overlay layers.
- **Privacy Guarantee**: No individual trajectory reconstructable from published maps.

## 11.7 Privacy & Compliance Module
- **Responsibility**: Enforce data governance and user control.
- **Implementation**:
  - Granular consent toggles: "Share location with contacts", "Contribute to Fear Map", "Enable AI analysis".
  - Data retention policies: Auto-delete raw sensor logs after 24h; retain only aggregated scores for 30 days.
  - Right-to-erasure: One-tap account deletion cascades to all Firestore collections via Cloud Function.

---

# 12. AI Model & Danger Score Logic

## 12.1 Google Gemini Integration Strategy
SafeHer leverages **Google Gemini Pro** for contextual risk reasoning, chosen for its:
- Strong natural language understanding of situational nuance.
- Low-latency inference suitable for real-time safety applications.
- Flexible prompt engineering for structured output parsing.

### 12.1.1 Input Context Vector Schema
The system constructs a structured JSON context object for AI inference:

```json
{
  "user_context": {
    "time_utc": "2026-04-25T22:15:00Z",
    "local_time": "22:15",
    "day_of_week": "Saturday"
  },
  "location_context": {
    "latitude": 28.6139,
    "longitude": 77.2090,
    "accuracy_meters": 15,
    "semantic_type": "residential_alley",  // classified via reverse-geocoding + POI API
    "isolation_score": 0.85,  // 0=crowded, 1=deserted
    "nearby_poi_count": 2
  },
  "motion_context": {
    "current_speed_kmph": 3.2,
    "velocity_variance_2min": 1.8,
    "route_deviation_meters": 210,
    "abrupt_stop_detected": true,
    "motion_pattern": "erratic_walking"
  },
  "environmental_context": {
    "network_signal_dbm": -105,
    "battery_level_percent": 42,
    "screen_state": "off"
  },
  "rule_based_score": 45  // Pre-computed edge score (0-50)
}
```

### 12.1.2 Prompt Engineering for Structured Output
To ensure reliable parsing, the system uses a constrained prompt template:

```
You are a safety risk assessment AI. Analyze the following contextual data for a woman traveling alone. 
Output ONLY a valid JSON object with two fields:
{
  "risk_score": <integer 0-50>,
  "justification": "<one-sentence explanation>"
}

Context:
{context_vector_json}

Rules:
- Score 0 = completely safe, 50 = extreme imminent danger
- Consider time, location isolation, motion anomalies, and network status
- Do not output any text outside the JSON object
```

### 12.1.3 Output Parsing & Normalization
```python
# Pseudocode: AI Response Handling
def parse_gemini_response(api_response):
    try:
        result = json.loads(api_response.text)
        ai_score = min(max(int(result['risk_score']), 0), 50)  # Clamp to [0,50]
        justification = result['justification'][:200]  # Truncate for logging
        return {'ai_score': ai_score, 'reason': justification}
    except (JSONDecodeError, KeyError, ValueError):
        # Fallback to rule-based only
        log_error("Gemini parse failed", api_response.text)
        return {'ai_score': 0, 'reason': "AI fallback: parsing error"}
```

## 12.2 Hybrid Score Fusion Algorithm
```python
def compute_final_danger_score(rule_score, ai_score, user_profile):
    # Dynamic weighting based on user history (optional)
    alpha = user_profile.get('rule_weight', 0.5)
    beta = 1.0 - alpha
    
    # Weighted fusion
    fused = (alpha * rule_score) + (beta * ai_score)
    
    # Apply user-specific threshold calibration
    calibrated = apply_personal_calibration(fused, user_profile)
    
    return min(max(round(calibrated), 0), 100)  # Final score ∈ [0,100]
```

## 12.3 Rule-Based Fallback Logic
To ensure system reliability during AI service outages or parsing failures:

```
IF Gemini_API_unavailable OR response_parse_error:
    Final_Score = rule_score * 2.0  # Scale rule-only score to [0,100]
    Alert_Threshold = 50  # Conservative threshold for rule-only mode
    Log: "AI fallback activated"
ELSE:
    Final_Score = hybrid_fusion(rule_score, ai_score)
    Alert_Threshold = get_user_threshold()  # Default 60
```

This fallback guarantees continuous operation with degraded but functional risk assessment, adhering to safety-critical system design principles [12].

## 12.4 Ethical AI Considerations
- **Bias Mitigation**: Prompt examples are audited for demographic neutrality; location classification avoids socioeconomic profiling.
- **Explainability**: Justification strings are logged (not shown to users by default) for model debugging and transparency audits.
- **Human-in-the-Loop**: All autonomous alerts include a 30-second user-cancel window (configurable) to prevent false escalations.