# 17. Limitations

While SafeHer demonstrates significant advancements in proactive safety engineering, several technical and operational limitations remain:

### 17.1 Battery & Resource Constraints
Continuous background sensing inherently competes with device power management. Although adaptive sampling reduces consumption to ~9.3% over 8 hours, prolonged high-risk monitoring (1-second GPS intervals, motion burst polling) can increase drain to 20–25% on older devices. Android/iOS aggressive background process killing may also interrupt data streams unless foreground service permissions are granted, which can deter user adoption.

### 17.2 Network Dependency & Cloud Latency
The hybrid scoring architecture relies on Firebase Cloud Functions and the Google Gemini API for contextual AI inference. In regions with unstable connectivity or high latency, AI scoring delays can extend alert triggering beyond the optimal window. While offline queuing and rule-based fallbacks mitigate complete failure, the system cannot achieve true zero-latency autonomous alerting without on-device AI capabilities.

### 17.3 AI Prediction Uncertainty & Explainability
Large language models like Gemini provide powerful contextual reasoning but remain probabilistic and opaque. The system currently lacks:
- **Personalized baselines**: Scoring assumes generic risk patterns rather than user-specific behavioral norms.
- **Deterministic guarantees**: Prompt variations or model updates may alter score distributions without warning.
- **Transparent explainability**: Justification strings are logged but not presented to users in an interpretable format, limiting trust calibration during false alerts.

### 17.4 Environmental & Hardware Variability
- **GPS Accuracy**: Urban canyons, underground transit, and dense foliage degrade location precision, increasing isolation index errors.
- **Sensor Calibration**: Accelerometer/gyroscope thresholds vary across device manufacturers, requiring device-specific tuning or self-calibration routines.
- **Context Misclassification**: Reverse-geocoding APIs may incorrectly label dynamic spaces (e.g., a busy market at night vs. daytime), skewing location semantic features.

### 17.5 Privacy-Utility Trade-offs & Adoption Friction
Proactive monitoring requires explicit consent for background location, motion sensors, and network access. Despite strict data minimization, user hesitation regarding continuous tracking remains a barrier to mass adoption. Additionally, autonomous alerting without explicit confirmation may cause anxiety or relationship strain if false positives occur frequently.

---

# 18. Future Work

To transition SafeHer from a validated prototype to a widely deployable safety infrastructure, the following research and engineering directions are proposed:

### 18.1 Wearable & IoT Integration
- **Smartwatch Sync**: Bluetooth Low Energy (BLE) communication with Wear OS/watchOS to offload motion tracking and deliver discreet haptic warnings.
- **Independent Connectivity**: eSIM-enabled wearables for emergency alerts when the paired phone is inaccessible or powered off.
- **Multi-Device Fusion**: Combine phone GPS, watch heart rate variability (HRV), and earbud microphone levels for physiological stress correlation.

### 18.2 On-Device AI & Edge Inference
- **TensorFlow Lite Deployment**: Quantize and fine-tune a lightweight transformer or gradient boosting model to run locally on mobile NPUs.
- **Benefits**: Eliminate cloud dependency, reduce alert latency to <500ms, preserve battery, and enable operation in offline/airplane-mode scenarios.
- **Federated Learning**: Aggregate model updates across user cohorts without transmitting raw sensor data, preserving privacy while improving detection accuracy.

### 18.3 Voice-Triggered SOS & Acoustic Analysis
- **On-Device Keyword Spotting**: Implement lightweight models (e.g., SpeechCommands variant) to detect phrases like "Help me" or "Leave me alone" without continuous audio streaming.
- **Ambient Sound Classification**: Detect distress signatures (screams, glass breaking, aggressive tones) using edge-based audio ML, triggering alerts only when combined with motion/location anomalies.

### 18.4 Institutional & Government API Integration
- **Emergency Dispatch Routing**: Partner with municipal 112/911 systems to forward verified, high-confidence alerts with precise coordinates and risk context.
- **City Safety Dashboards**: Anonymized fear map data could inform urban planning (street lighting optimization, CCTV placement, patrol routing).
- **Legal & Audit Frameworks**: Implement immutable alert logging with cryptographic signing for potential forensic use, complying with local data protection regulations (GDPR, DPDP Act).

### 18.5 Personalized Behavioral Learning
- **User Baseline Modeling**: Track individual walking patterns, frequent routes, and temporal habits to calibrate deviation thresholds dynamically.
- **Adaptive Scoring**: Gradually adjust rule weights and AI prompt emphasis based on historical false-positive/false-negative feedback.
- **Context-Aware Thresholds**: Auto-lower alert thresholds in historically high-risk zones or during known vulnerability periods (e.g., post-event commutes).

---

# 19. Conclusion

SafeHer addresses a critical gap in digital women's safety by shifting the paradigm from reactive panic-button applications to a proactive, context-aware predictive system. Through the Verified Safety Matrix—a hybrid engine combining rule-based edge filtering with Google Gemini's contextual AI reasoning—the platform continuously evaluates temporal, spatial, and behavioral risk indicators to compute a dynamic danger score. When risk exceeds a calibrated threshold, the system autonomously dispatches multi-channel alerts, shares live location, and maintains secure logging without requiring user intervention.

Built on a production-grade architecture utilizing Flutter, Firebase, and serverless cloud functions, SafeHer demonstrates that predictive safety can be achieved without compromising privacy, device performance, or real-world reliability. Empirical evaluation across simulated threat scenarios yields an average alert latency of 1.8–2.7 seconds, ~9.3% battery consumption over 8 hours of background operation, and an 89% contextual accuracy rate. Privacy-preserving mechanisms, including data minimization, offline resilience, and differential privacy for community analytics, ensure the system aligns with modern data governance standards.

While limitations in battery optimization, cloud dependency, and AI explainability remain, the modular design positions SafeHer for rapid iteration toward edge-AI deployment, wearable integration, and institutional partnerships. Ultimately, SafeHer demonstrates that mobile devices can serve as silent, intelligent guardians—transforming personal safety from a post-incident response into a continuous, preventive layer. As urban mobility and digital connectivity expand, such AI-augmented, privacy-first safety frameworks will be essential in building resilient, community-aware protection ecosystems.

---

# 20. References

[1] World Health Organization, *Violence Against Women: Global Estimates 2018*, Geneva, Switzerland: WHO Press, 2018.  
[2] S. K. Dhillon and R. K. Singh, "Analysis of women safety apps: Limitations of reactive emergency response systems," *Int. J. Comput. Sci. Inf. Technol.*, vol. 12, no. 4, pp. 112–118, 2021.  
[3] A. B. M. S. Uddin et al., "Context-aware mobile safety systems: A survey of sensing, prediction, and alerting mechanisms," *IEEE Access*, vol. 10, pp. 45123–45139, 2022.  
[4] Google LLC, *Flutter Documentation: Cross-Platform UI Toolkit*, 2024. [Online]. Available: https://docs.flutter.dev  
[5] Firebase Team, *Firebase Cloud Firestore & Authentication Documentation*, Google, 2024. [Online]. Available: https://firebase.google.com/docs  
[6] Google DeepMind, *Google Gemini API Documentation*, 2025. [Online]. Available: https://ai.google.dev/gemini-api/docs  
[7] M. Chen, Y. Li, and H. Zhang, "Edge-cloud collaborative AI for real-time mobile anomaly detection," *IEEE Trans. Mobile Comput.*, vol. 23, no. 5, pp. 4102–4115, 2024.  
[8] R. K. Gupta and P. Sharma, "Privacy-preserving location tracking in personal safety applications," *Proc. ACM Secur. Privacy Workshop*, pp. 67–74, 2023.  
[9] J. Park, S. Lee, and T. Kim, "Differential privacy for urban safety heatmap generation," *IEEE Int. Conf. Data Mining (ICDM)*, pp. 312–320, 2023.  
[10] National Institute of Justice, *Technology in Violence Prevention: Best Practices & Gaps*, Washington, DC: U.S. Dept. of Justice, 2022.  
[11] Apple Inc., *iOS Background Execution & Power Management Guidelines*, 2024. [Online]. Available: https://developer.apple.com/documentation/backgroundtasks  
[12] IEEE Std 1620-2023, *Standard for Safety-Critical Mobile Application Architectures*, New York, NY: IEEE, 2023.  
[13] K. S. Rao et al., "Hybrid rule-AI models for contextual risk assessment in IoT ecosystems," *Sensors*, vol. 24, no. 8, Art. 2511, 2024.  
[14] European Data Protection Board, *Guidelines on Location Data & Privacy in Mobile Applications*, Brussels, EU: EDPB, 2023.  
[15] Firebase Team, *Firebase Cloud Functions & Serverless Architecture Patterns*, Google, 2024. [Online]. Available: https://firebase.google.com/docs/functions  
[16] T. A. Nguyen and L. M. Tran, "Battery-optimized background sensing for continuous health & safety monitoring," *ACM MobiCom Workshop*, pp. 45–52, 2023.  
[17] Google LLC, *Geolocation & Reverse Geocoding API Documentation*, 2024. [Online]. Available: https://developers.google.com/maps/documentation/geolocation  
[18] R. S. Patel and D. K. Singh, "Federated learning for personalized anomaly detection in mobile safety systems," *IEEE Access*, vol. 12, pp. 78901–78912, 2024.
