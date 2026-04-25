from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_research_paper():
    document = Document()

    # Apply global styling for Academic standard (Times New Roman, 12pt)
    style = document.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)

    # Title
    title = document.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title.add_run('SafeHer: A Proactive and AI-Driven Mobile Safety System for Women\n')
    title_run.bold = True
    title_run.font.size = Pt(16)

    # Author/Info (Replace with your actual details)
    author = document.add_paragraph()
    author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    author_run = author.add_run('[Your Name]\n[Your College/University Name]\n[Your Department]\n[2024]')
    author_run.italic = True

    # Helper function to add justified paragraphs
    def add_justified_paragraph(text, style=None):
        p = document.add_paragraph(text, style=style)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        return p

    # Abstract
    document.add_heading('Abstract', level=1)
    add_justified_paragraph(
        "Women's safety in urban and semi-urban environments remains a pressing global issue. Traditional mobile safety solutions predominantly rely on reactive mechanisms, requiring victims to manually trigger an SOS alert during a critical incident. Such systems often fail in real-world scenarios where victims are unable to access their devices or face delayed reactions due to panic. This paper presents SafeHer, a proactive and predictive mobile safety application based on the Verified Safety Matrix. By continuously monitoring user context through mobile sensors and leveraging Google Gemini's AI for risk analysis, the system generates a real-time Danger Score (0–100). When the risk exceeds a predefined threshold, the system autonomously triggers alerts, notifying trusted contacts without requiring user intervention. Built on a robust Flutter architecture with Firebase cloud infrastructure, SafeHer represents a paradigm shift from reactive emergency applications to preventive, automated safety systems."
    )

    # 1. Introduction
    document.add_heading('1. Introduction', level=1)
    add_justified_paragraph(
        "The safety of individuals, particularly women navigating isolated or late-night scenarios, is a critical societal challenge. With the proliferation of smartphones, numerous safety applications have been developed. However, the vast majority of these technological interventions—such as panic button applications or emergency dialers—are fundamentally reactive. They operate on the assumption that a user in imminent danger will have the presence of mind, time, and physical capability to activate an alert.\n"
        "In actual escalations, perpetrators often prevent access to mobile devices, rendering manual-trigger systems ineffective. To address this critical gap, we introduce SafeHer, an intelligent mobile application designed to predict and prevent danger before it becomes critical. By utilizing continuous contextual monitoring and AI-powered risk analysis, SafeHer shifts the personal safety paradigm from a reactive approach to a proactive, automated defense mechanism."
    )

    document.add_heading('1.1 Problem Statement', level=2)
    document.add_paragraph("Existing safety systems fail to provide preventive security because they rely entirely on user-initiated triggers. Key limitations include:")
    document.add_paragraph("Physical Constraints: Inability to access the phone during an attack.", style='List Bullet')
    document.add_paragraph("Psychological Factors: Delayed reactions due to panic or shock.", style='List Bullet')
    document.add_paragraph("Lack of Predictive Capabilities: No system exists to identify and warn the user of an escalating threat before the situation becomes critical.", style='List Bullet')

    document.add_heading('1.2 Objectives', level=2)
    document.add_paragraph("The primary objective of this research is to design, implement, and evaluate a production-grade mobile safety system that:")
    document.add_paragraph("Continuously monitors contextual data (location, motion, time).", style='List Bullet')
    document.add_paragraph("Employs an AI engine to dynamically compute a real-time Danger Score.", style='List Bullet')
    document.add_paragraph("Automatically dispatches SOS alerts and real-time tracking to trusted contacts when a danger threshold is breached.", style='List Bullet')
    document.add_paragraph("Ensures data privacy, offline resilience, and optimized battery consumption.", style='List Bullet')

    # 2. Architecture
    document.add_heading('2. Proposed System Architecture: The Verified Safety Matrix', level=1)
    add_justified_paragraph(
        "The core innovation of SafeHer is the Verified Safety Matrix, a predictive engine that correlates multiple data points to assess risk continuously. The system is built using a modern mobile technology stack comprising Flutter for the frontend, Firebase for robust cloud services, and the Google Gemini API for AI-based contextual analysis."
    )

    document.add_heading('2.1 Core Modules', level=2)
    add_justified_paragraph("1. Secure Authentication: Ensures that only verified users have access to the system using Firebase phone-based OTP authentication, preventing unauthorized access or spoofing.")
    add_justified_paragraph("2. Continuous Contextual Monitoring: Leverages mobile GPS and motion sensors to track user movements securely. Data is persisted in Firestore, enabling real-time live monitoring during emergencies.")
    add_justified_paragraph("3. Emergency SOS & Trusted Contacts: A foundational layer allowing users to manage a secure list of emergency contacts. These contacts receive instant notifications containing the user's live location and emergency status via Firebase Cloud Messaging (FCM).")

    document.add_heading('2.2 The Danger Score Engine', level=2)
    add_justified_paragraph("The Danger Score Engine is the intelligence hub of SafeHer, operating in two distinct phases to balance efficiency and accuracy:")
    document.add_paragraph("Phase 1: Rule-Based Logic: The system applies deterministic rules to detect anomalies. For instance, being in an isolated area at a late hour, sudden erratic changes in motion, or an unexpected drop in speed in a high-risk zone generate intermediate risk flags.", style='List Bullet')
    document.add_paragraph("Phase 2: AI-Powered Analysis (Google Gemini): Contextual data—including time of day, location categorization, speed of travel, and movement patterns—is fed into the Google Gemini Large Language Model (LLM). The model processes this complex context to compute a dynamic Danger Score (0–100).", style='List Bullet')

    document.add_heading('2.3 Automated Alert Mechanism', level=2)
    add_justified_paragraph(
        "When the Danger Score exceeds a critical threshold (e.g., >60), the system transitions into an active alert state. It autonomously dispatches SOS notifications, bypassing the need for manual user interaction. This fail-safe ensures that help is summoned even if the user is incapacitated."
    )

    # 3. Implementation
    document.add_heading('3. Implementation and Production Readiness', level=1)
    add_justified_paragraph(
        "Unlike theoretical prototypes, SafeHer was developed utilizing a production-ready engineering methodology, ensuring high availability and reliability in critical situations."
    )

    document.add_heading('3.1 The Fear Map (Community Safety Layer)', level=2)
    add_justified_paragraph("SafeHer incorporates a 'Fear Map,' which aggregates anonymized risk data to generate heatmaps of unsafe areas using location clusters. This community-driven feature helps users make informed navigational decisions and serves as a macro-level tool for analyzing city-wide safety.")

    document.add_heading('3.2 Offline Support and Fail-Safes', level=2)
    add_justified_paragraph("Recognizing that emergencies often occur in areas with poor network connectivity, SafeHer utilizes Firestore's offline persistence. If an automated SOS is triggered while offline, the request is queued locally and instantly transmitted via a retry mechanism once a connection is re-established.")

    document.add_heading('3.3 Optimized Background Execution', level=2)
    add_justified_paragraph("Continuous sensor monitoring traditionally drains battery life, leading users to uninstall safety apps. SafeHer implements battery-aware tracking algorithms to ensure the application remains active in the background without severely impacting device performance.")

    document.add_heading('3.4 Cloud Automation, Logging, and Security', level=2)
    add_justified_paragraph("Backend logic is abstracted to Firebase Cloud Functions, ensuring secure and scalable processing of the Danger Score without exposing API keys on the client side. Strict Firestore security rules are implemented to maintain end-to-end data protection. Additionally, Firebase Crashlytics is integrated for logging alert success rates, app performance, and real-time error tracking.")

    # 4. Discussion
    document.add_heading('4. Discussion', level=1)
    add_justified_paragraph(
        "The transition from a reactive manual trigger to an automated, AI-driven predictive system addresses the fundamental flaw in traditional safety applications. By actively monitoring the user's environment, SafeHer functions as a proactive digital bodyguard.\n"
        "The integration of Google Gemini allows for a nuanced understanding of context that rigid rule-based systems lack. For example, a slow walking speed in a crowded commercial district at 2:00 PM indicates normal behavior, but the same speed in an unlit, isolated alley at 2:00 AM is highly suspicious. The AI effectively differentiates between these scenarios, reducing false positives while maintaining high sensitivity to actual threats."
    )

    # 5. Future Enhancements
    document.add_heading('5. Future Enhancements', level=1)
    document.add_paragraph("The current iteration of SafeHer establishes a robust foundation for proactive safety. Future work will focus on expanding the Verified Safety Matrix:")
    document.add_paragraph("Voice-Triggered SOS: Implementing offline Natural Language Processing (NLP) to detect distress phrases (e.g., 'Help me', 'Leave me alone').", style='List Bullet')
    document.add_paragraph("Wearable Integration: Extending sensor data collection to smartwatches to monitor biometric stress indicators, such as sudden heart rate spikes.", style='List Bullet')
    document.add_paragraph("Behavioral Learning: Training the AI on individual user routines to better detect anomalies and deviations from normal commuting behavior.", style='List Bullet')
    document.add_paragraph("Institutional APIs: Developing direct integration with law enforcement and emergency medical dispatch systems for faster response times.", style='List Bullet')

    # 6. Conclusion
    document.add_heading('6. Conclusion', level=1)
    add_justified_paragraph(
        "SafeHer demonstrates the viability and absolute necessity of predictive safety systems in the modern era. By combining mobile sensor technology, scalable cloud infrastructure, and advanced AI models, the application successfully identifies potential threats before they escalate into critical emergencies. This project not only provides a scalable, production-ready solution for personal safety but also lays the necessary groundwork for the future of intelligent, automated security systems in smart cities."
    )
    
    # 7. References
    document.add_heading('7. References', level=1)
    document.add_paragraph("[1] Add citation on Mobile Sensor Tracking for safety here.", style='List Bullet')
    document.add_paragraph("[2] Add citation on AI implementations in Mobile Applications here.", style='List Bullet')
    document.add_paragraph("[3] Add citation on existing Women's Safety Apps limitations here.", style='List Bullet')

    # Save document
    document.save('SafeHer_Research_Paper.docx')
    print("Document successfully generated: SafeHer_Research_Paper.docx")

if __name__ == '__main__':
    create_research_paper()
