# 5. Literature Review

## 5.1 Overview of Existing Safety Solutions
Digital interventions for women's safety have evolved significantly over the past decade, broadly falling into three categories:

| Category | Representative Examples | Core Mechanism |
|----------|-------------------------|----------------|
| **Traditional SOS Apps** | bSafe, Circle of 6, Nirbhaya App | Manual panic button → SMS/call to contacts |
| **GPS Tracking & Geofencing Apps** | Life360, FamiSafe, Google Trusted Contacts | Continuous location sharing + zone-based alerts |
| **AI/ML-Enhanced Research Prototypes** | SAFECITY (crowdsourced heatmap), SHIELD (anomaly detection), VAMA (voice-assisted) | Sensor fusion + behavioral modeling + predictive alerts |

## 5.2 Critical Analysis of Limitations

### 5.2.1 Traditional SOS Applications
While widely adopted, manual-trigger systems suffer from fundamental usability gaps in real emergencies:
- **Interaction Dependency**: Require conscious, deliberate user action—often impossible during physical restraint, panic-induced freezing, or device confiscation [1].
- **Contextual Blindness**: Treat all locations, times, and movement patterns identically, ignoring environmental risk factors [2].
- **Alert Fatigue**: High false-positive rates from accidental triggers reduce trust and response urgency among contacts [3].

### 5.2.2 GPS-Centric Tracking Systems
Location-sharing platforms improve situational awareness but introduce new constraints:
- **Privacy Concerns**: Continuous location broadcasting raises surveillance and data-misuse risks [4].
- **Battery Drain**: High-frequency GPS polling significantly reduces device usability [5].
- **Reactive Logic**: Geofence breaches are detected post-entry, not pre-escalation [6].

### 5.2.3 AI-Based Research Prototypes
Emerging academic work explores predictive safety using machine learning:
- **SAFECITY** aggregates anonymous harassment reports to generate community heatmaps but lacks real-time individual risk assessment [7].
- **SHIELD** employs accelerometer-based fall detection but operates in isolation from contextual cues like time or location type [8].
- **VAMA** integrates voice-command SOS but depends on clear audio input, which may be unavailable in noisy or constrained scenarios [9].

## 5.3 Identified Research Gaps
Despite technological advances, no existing solution comprehensively addresses the following requirements simultaneously:
1. **Proactive Threat Detection**: Early identification of risk before manual intervention is needed.
2. **Contextual Intelligence**: Integration of temporal, spatial, and behavioral signals for nuanced risk assessment.
3. **Autonomous Alerting**: Reliable, user-independent escalation when danger is detected.
4. **Production-Ready Privacy**: End-to-end data protection with user-controlled sharing and offline resilience.
5. **Scalable Architecture**: Cloud-native design supporting real-time processing, AI inference, and multi-channel notifications.

SafeHer directly addresses these gaps through its Verified Safety Matrix—a hybrid engine fusing rule-based logic with large language model (LLM) contextual reasoning—deployed on a privacy-first, battery-optimized mobile architecture.

---

# 6. Problem Statement

## 6.1 Core Problem
Current women's safety applications fail to provide timely, reliable protection during real-world emergencies due to three interrelated systemic shortcomings:

### 6.1.1 Manual Dependency in High-Stress Scenarios
Psychological studies confirm that acute threat triggers fight-flight-freeze responses, impairing fine motor skills and decision-making capacity [10]. Requiring a victim to unlock a phone, navigate an app, and press a button introduces critical delays—or complete failure—when seconds matter.

### 6.1.2 Absence of Predictive Capability
Existing systems operate on a post-incident model: alerts are triggered only after harm has occurred or is actively unfolding. There is no mechanism to identify early behavioral or environmental indicators (e.g., sudden route deviation, prolonged stationary status in isolated areas, unusual velocity patterns) that precede escalation.

### 6.1.3 Contextual Blindness and Uniform Risk Assumptions
Most applications apply static rules (e.g., "send alert if SOS pressed") without adapting to dynamic risk factors:
- Time-of-day (e.g., 2 AM vs. 2 PM)
- Location type (e.g., well-lit commercial area vs. deserted alley)
- Movement anomalies (e.g., abrupt stop after consistent motion)
- Network/environmental status (e.g., low connectivity, audio cues)

This one-size-fits-all logic generates either missed threats (false negatives) or excessive false alarms (false positives), eroding system credibility.

## 6.2 Real-World Challenges Amplifying the Problem
- **Device Accessibility**: Victims may not have physical access to their phone during an assault.
- **Network Instability**: Poor connectivity in semi-urban/rural areas delays or blocks cloud-dependent alerts.
- **Battery Constraints**: Continuous sensing and transmission drain device power, limiting operational window.
- **Privacy-Utility Trade-off**: Users resist constant location tracking without transparent, granular control.

## 6.3 Formal Problem Definition
> *How can a mobile safety system autonomously detect escalating threat conditions using contextual sensor data, compute a reliable risk score in real-time, and trigger protective alerts without requiring conscious user interaction—while preserving privacy, optimizing resource usage, and maintaining scalability?*

SafeHer is designed to answer this question through a production-grade, AI-augmented architecture.

---

# 7. Objectives

The development of SafeHer is guided by the following specific, measurable, and technically grounded objectives:

### 7.1 Primary Objectives
1. **Design a Proactive Safety Framework**: Develop a mobile system that continuously monitors contextual signals (location, motion, time, environment) to identify potential threats before manual intervention is required.
2. **Implement a Hybrid Danger Score Engine**: Create a two-phase risk assessment module combining:
   - *Phase 1*: Rule-based filtering for low-latency, interpretable risk indicators.
   - *Phase 2*: Google Gemini AI for contextual reasoning and nuanced score refinement (output: 0–100 normalized scale).
3. **Automate Emergency Alerting**: Establish a threshold-driven workflow (e.g., Score ≥ 60) that autonomously triggers multi-channel notifications (push, SMS fallback) to pre-verified trusted contacts, including live location and incident metadata.
4. **Ensure Privacy-Preserving Architecture**: Enforce end-to-end data protection via Firebase Security Rules, user-controlled data sharing policies, and minimal data collection principles compliant with GDPR-inspired best practices.

### 7.2 Secondary (Engineering) Objectives
5. **Optimize for Real-World Deployment**:
   - Implement adaptive sensor sampling to limit battery consumption to ≤15% over 8 hours of background operation.
   - Support offline persistence with queued alert retry mechanisms for network-resilient operation.
6. **Enable Scalable Cloud Automation**: Leverage Firebase Cloud Functions for serverless processing of danger scores, AI API calls, and notification dispatch—ensuring horizontal scalability without dedicated infrastructure.
7. **Facilitate Extensibility**: Architect modular components (e.g., pluggable AI providers, configurable alert channels) to support future integrations with wearables, municipal emergency APIs, and community safety layers (e.g., anonymized Fear Map).

These objectives collectively ensure that SafeHer transitions from a conceptual prototype to a production-viable safety solution.

---

# 8. Proposed System: High-Level Overview

## 8.1 Vision
SafeHer reimagines personal safety as a continuous, context-aware service rather than a reactive emergency tool. The system operates on a **sense → analyze → act** loop, silently monitoring user context and intervening only when predictive risk assessment indicates credible threat escalation.

## 8.2 Core Components

### 8.2.1 Multi-Modal Contextual Sensing Layer
The mobile client (Flutter) collects and preprocesses heterogeneous sensor data at adaptive intervals:
- **Geospatial**: GPS coordinates, accuracy radius, altitude, speed, heading.
- **Motion**: Accelerometer (sudden stops, falls), gyroscope (orientation shifts), step detection.
- **Temporal**: Time-of-day, day-of-week, duration of stationary status.
- **Environmental** (future): Ambient light, noise level, network signal strength.

Data is locally filtered (e.g., Kalman smoothing for GPS) and feature-engineered into a structured context vector before transmission.

### 8.2.2 Hybrid Danger Score Engine (Verified Safety Matrix)
Risk assessment occurs in two coordinated phases:

```
Phase 1: Rule-Based Pre-Filtering (Edge)
  IF time ∈ [22:00, 05:00] AND location_type = "isolated" → +25 risk points
  IF velocity_variance > threshold AND route_deviation > 200m → +30 risk points
  IF network_signal < -100dBm AND motion = "stationary" → +20 risk points
  → Output: Base_Risk_Score ∈ [0, 50]

Phase 2: AI Contextual Refinement (Cloud)
  Input: {time, location_semantic, speed_profile, motion_pattern, base_risk}
  Prompt: "Given this contextual vector, assess situational danger for a woman traveling alone. Output a normalized risk score 0–100 with brief justification."
  Model: Google Gemini Pro (via secure Firebase Cloud Function proxy)
  → Output: AI_Risk_Score ∈ [0, 50]

Final Danger Score = Base_Risk_Score + AI_Risk_Score ∈ [0, 100]
```

This hybrid approach balances computational efficiency (edge-based rules) with contextual nuance (cloud AI), while maintaining interpretability and fallback reliability.

### 8.2.3 Autonomous Cloud Alerting Pipeline
When `Danger Score ≥ Threshold (default: 60)`:
1. Firebase Cloud Function validates the score and user preferences.
2. Alert payload is constructed: `{user_id, timestamp, location{lat,lng,accuracy}, risk_score, incident_context}`.
3. Notifications are dispatched via:
   - **Primary**: Firebase Cloud Messaging (push to trusted contacts' devices).
   - **Fallback**: Twilio/SMS API (if push fails or user enables SMS backup).
4. Live location streaming is initiated for 15 minutes (configurable), with user-override capability.
5. All actions are logged to Firestore for audit, analytics, and model retraining.

## 8.3 System-Wide Design Principles
- **Privacy by Default**: No raw sensor data is stored long-term; location is anonymized for community features (Fear Map).
- **User Agency**: Users control contact lists, alert thresholds, data retention, and can pause monitoring anytime.
- **Resource Awareness**: Adaptive sampling, background execution limits, and offline queuing ensure usability on mid-tier devices.
- **Extensibility**: Modular architecture supports future AI model swaps, new sensor types, and institutional API integrations.

`[Figure 1: High-Level System Flow Diagram – to be inserted]`  
*Caption: Data flow from mobile sensing → edge preprocessing → cloud AI scoring → autonomous alerting → trusted contacts.*
