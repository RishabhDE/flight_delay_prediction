# Flight Delay Prediction MLOps System
## Video Presentation Slide Content (12 minutes)

---

## SLIDE 1: Title Slide
**Flight Delay Prediction - Production MLOps System**

Team: FlightGuard AI (Group #5)
- Rishabh Malik
- Aleena Varghese

Course: AAI-540 Machine Learning Operations
Date: October 21, 2025

**Speaker: Rishabh (30 seconds)**
"Hello, I'm Rishabh Malik, and together with my teammate Aleena, we'll demonstrate our complete MLOps system for flight delay prediction built on AWS SageMaker."

---

## SLIDE 2: Business Problem & Use Case
**Why Flight Delay Prediction?**

- Flight delays cost airlines **$8+ billion annually**
- Frustrates millions of passengers
- Cascading effects throughout air network

**Our Solution:**
- Predict delays **before departure** (≥15 minutes)
- Enable proactive operational adjustments
- Improve passenger communication and satisfaction

**Real-World Impact:**
- Airlines: Optimize crew, gates, maintenance
- Passengers: Make alternative arrangements early

**Speaker: Rishabh (1 minute)**
"Flight delays are a massive problem. Our ML system predicts whether a flight will be delayed before departure, allowing airlines to proactively adjust operations and notify passengers early. This is not just a model - it's a complete production system with monitoring and CI/CD."

---

## SLIDE 3: System Architecture Overview
**Complete MLOps Pipeline**

```
Real Data (5.5M records) 
    ↓
Feature Store (Unified)
    ↓
Model Training (3 algorithms tested)
    ↓
Model Registry
    ↓
Quality Gate (CI/CD Pipeline)
    ↓
Deployment (Real-time Endpoint)
    ↓
Monitoring (Hourly + CloudWatch)
    ↓
Batch Inference (Business Insights)
```

**Key Components:**
- AWS SageMaker Feature Store
- Real-time endpoint (ml.m5.large)
- CloudWatch monitoring with alarms
- SageMaker Pipelines for CI/CD
- Batch processing for operational planning

**Speaker: Aleena (1 minute)**
"Our architecture follows MLOps best practices. We start with real data from Mendeley - 5.5 million flight records - then use Feature Store for consistent feature access, train multiple models, deploy the best one through a CI/CD pipeline with quality gates, and continuously monitor performance. Let me show you each component."

---

## SLIDE 4: Data Source - Real Dataset
**Mendeley Dataset (NOT Synthetic!)**

- **Source:** "Dataset for Airline Departure Delay Prediction"
- **Volume:** 5.5 million flight records from 2023
- **URL:** https://data.mendeley.com/datasets/xxwzw3tyfp/1
- **Sample:** 50,000 records for training
- **Delay Rate:** 22.48% (realistic distribution)

**Features (12 total):**
- Flight: airline, origin, destination, distance
- Temporal: day_of_week, month, departure_hour
- Weather: temperature, wind_speed, precipitation, visibility, snow

**Why Real Data Matters:**
✅ Realistic delay patterns
✅ Real airline/airport distributions
✅ Actual weather correlations
✅ Production-ready insights

**Speaker: Aleena (45 seconds)**
"Critical point - we use REAL data, not synthetic. This is the Mendeley dataset with 5.5 million actual flight records from 2023, including 18 airlines and over 350 airport pairs with weather conditions. This ensures our model reflects real-world patterns."

---

## SLIDE 5: Feature Store Demo
**AWS SageMaker Feature Store**

**Feature Group:** `flight-delay-features-2025-10-21-03-41-14`

**Design Decision: Unified Feature Group**
- Initially considered separate flight + weather groups
- **Simplified to single unified group** for better maintainability
- 50,000 records ingested successfully

**Architecture:**
- **Online Store:** Low-latency real-time retrieval (<10ms)
- **Offline Store:** Historical data for training (S3 Parquet)
- **Schema:** 12 features + event_time + record_id

**Demo Points to Show:**
1. Navigate to SageMaker → Feature Store
2. Show feature group with 50K records
3. Display feature schema and data types
4. Show online/offline store configuration

**Speaker: Rishabh (1.5 minutes)**
"Here's our Feature Store - you can see the unified feature group with 50,000 records. We have both online and offline stores. The online store gives us fast retrieval for real-time predictions, while the offline store provides historical data for model training and batch analysis. Notice the schema includes all 12 features we engineered."

---

## SLIDE 6: Model Training Results
**3 Models Evaluated**

| Model | F1-Score | Accuracy | ROC-AUC | Status |
|-------|----------|----------|---------|--------|
| Logistic Regression | 0.21 | 55.2% | 0.58 | ❌ Baseline |
| Random Forest | 0.33 | 63.4% | 0.64 | ⚠️ Good |
| **XGBoost** | **0.358** | **66.6%** | **0.663** | **✅ SELECTED** |

**XGBoost Performance Details:**
- Accuracy: 66.59%
- Precision: 26.82%
- Recall: 53.99%
- F1-Score: 0.358 ✅ (Target: ≥0.35)
- ROC-AUC: 0.663 ✅ (Target: ≥0.65)

**Why Conservative?**
- Predicts 34.7% delays vs actual 17.3%
- Better to warn customers than miss delays
- Business cost of false negative >> false positive

**Speaker: Aleena (1 minute)**
"We tested three algorithms. XGBoost won with F1-score of 0.358 and ROC-AUC of 0.663, meeting our targets. Notice the model is conservative - it over-predicts delays. This is intentional. Missing a delay and having angry passengers is much worse than a false alarm."

---

## SLIDE 7: Model Registry Demo
**SageMaker Model Registry**

**Model Package Group:** `FlightDelayPredictionPackageGroup`

**Registered Models:**
- XGBoost 1.7 with JSON booster format
- Preprocessing artifacts (scaler, encoders)
- Inference script with custom input/output handlers
- Model metadata and performance metrics

**Versioning & Approval:**
- Automatic versioning on each pipeline run
- Approval workflow (PendingManualApproval → Approved)
- Model lineage tracking

**Demo Points to Show:**
1. Navigate to SageMaker → Model Registry
2. Show model package group
3. Display model versions and approval status
4. Show model artifacts in S3

**Speaker: Rishabh (1 minute)**
"In the Model Registry, you can see our XGBoost model is registered with all artifacts - the model file, preprocessing components, and inference script. We have version control and an approval workflow. This ensures only validated models get deployed to production."

---

## SLIDE 8: Real-Time Endpoint Demo
**Deployed Endpoint**

**Configuration:**
- **Name:** `flight-delay-predictor-2025-10-21-06-04-56`
- **Instance:** ml.m5.large
- **Status:** InService ✅
- **Data Capture:** 100% enabled

**Sample Prediction:**
```json
Input: {
  "airline": "Alaska Airlines",
  "origin": "JFK",
  "destination": "SEA",
  "distance": 2422,
  "temperature": 45,
  "wind_speed": 12,
  ...
}

Output: {
  "predictions": [0],
  "probabilities": [[0.78, 0.22]]
}
```
**Result:** On-time (78% probability)

**Demo Points to Show:**
1. Navigate to SageMaker → Endpoints
2. Show endpoint InService status
3. Test with sample prediction
4. Show data capture enabled for monitoring

**Speaker: Aleena (1.5 minutes)**
"Here's our live endpoint. It's running on ml.m5.large and has been serving predictions reliably. Let me show you a test prediction - we input flight details like airline, route, weather conditions, and instantly get back a prediction with probabilities. Notice data capture is enabled at 100%, which feeds into our monitoring system."

---

## SLIDE 9: CloudWatch Monitoring Dashboard
**Real-Time Monitoring & Alarms**

**Dashboard:** `FlightDelayPrediction-ModelMonitoring`

**Key Metrics Tracked:**
- Invocations (requests per minute)
- Model Latency (<100ms target)
- 4xx/5xx Error Rates
- Invocation Errors

**Alarms Configured:**
1. **High Error Rate:** >10 errors per 10 minutes → SNS alert
2. **High Latency:** >1000ms → SNS alert

**Monitoring Schedule:**
- **Name:** `flight-delay-monitor-2025-10-21-06-25-01`
- **Frequency:** Hourly
- **Baseline:** 5,000 records with constraints
- **Detection:** Data drift, feature violations

**Demo Points to Show:**
1. Navigate to CloudWatch → Dashboards
2. Show real-time metrics (invocations, latency, errors)
3. Display configured alarms and their status
4. Show monitoring schedule in SageMaker

**Speaker: Rishabh (1.5 minutes)**
"Monitoring is crucial for production. Our CloudWatch dashboard shows real-time metrics - invocations, latency, errors. We have two alarms: one for high error rates and one for latency spikes. Additionally, we run hourly data quality monitoring that compares incoming data against our baseline to detect data drift. You can see the monitoring schedule is active and running."

---

## SLIDE 10: Model Monitoring Report
**Data Quality Monitoring Results**

**Baseline Creation:**
- 5,000 validation records
- Statistics: mean, std, min, max, distribution
- Constraints: threshold violations detected

**Monitoring Execution:**
- Hourly comparison against baseline
- Feature distribution analysis
- Constraint violation detection

**Sample Metrics:**
- Feature drift detection: ✅ Pass
- Data quality: ✅ Pass
- Missing value check: ✅ Pass
- Distribution shift: ⚠️ Minor (within tolerance)

**Visualization:**
- Monitoring report PNG showing metrics over time
- Baseline vs current data distributions
- Violation trends

**Speaker: Aleena (45 seconds)**
"Here's a sample monitoring report. Every hour, the system compares new data against our baseline to detect drift. You can see feature distributions, constraint checks, and violation alerts. This ensures our model continues to perform well as data patterns change over time."

---

## SLIDE 11: CI/CD Pipeline Demo
**SageMaker Pipeline with Quality Gates**

**Pipeline Name:** `FlightDelayPredictionPipeline`

**6 Steps:**
1. **Preprocessing** → Feature engineering, validation
2. **Training** → XGBoost model training
3. **Evaluation** → Calculate F1, accuracy, ROC-AUC
4. **Condition** → Quality gate check
5. **Register Model** → Add to registry if pass
6. **Fail Step** → Alert if quality not met

**Quality Gates:**
- F1-Score ≥ 0.35 ✅
- Accuracy ≥ 0.65 ✅

**Pipeline States Demonstrated:**
- ✅ **Success:** Model met thresholds → Deployed
- ❌ **Failure:** Degraded model → Pipeline stopped at gate

**Demo Points to Show:**
1. Navigate to SageMaker → Pipelines
2. Show pipeline graph (DAG visualization)
3. Display successful execution (green path)
4. Show failed execution (stopped at condition check)

**Speaker: Rishabh (1.5 minutes)**
"This is our CI/CD pipeline with 6 steps. The critical part is the quality gate - if the model's F1-score drops below 0.35 or accuracy below 65%, the pipeline automatically fails and prevents deployment. Here you can see a successful run where the model passed all checks and was registered. And here's a failed run where we intentionally used a degraded model - the pipeline correctly stopped at the condition check."

---

## SLIDE 12: Batch Inference Results
**Large-Scale Predictions for Business Insights**

**Batch Processing:**
- **Dataset:** 5,000 flights
- **Processing Time:** 42 seconds (using real-time endpoint)
- **Alternative:** Batch Transform (20+ minutes for demo, cost-effective for millions)

**Performance Metrics:**
- Accuracy: 72.16% ✅
- Precision: 34.83%
- Recall: 69.94%
- F1-Score: 46.50%
- ROC-AUC: 78.13%

**Business Insights:**
- **High-Risk Flights:** 251 flights (5%) with >70% delay probability
- **Conservative Predictions:** 34.7% predicted delays vs 17.3% actual
- **Airline Variations:** Accuracy ranges 68-76% across carriers

**Use Cases:**
- Daily operational planning
- Proactive passenger notifications
- Route performance analysis
- Crew and gate optimization

**Speaker: Aleena (1 minute)**
"For operational planning, we ran batch inference on 5,000 flights. It completed in just 42 seconds and achieved 72% accuracy. The system identified 251 high-risk flights with over 70% delay probability - these are perfect candidates for proactive passenger communication. Notice the model continues its conservative approach, which is exactly what we want for business operations."

---

## SLIDE 13: Visualization - Batch Results
**Comprehensive Analysis Dashboard**

**4-Panel Visualization:**

1. **Confusion Matrix**
   - True On-Time: 3,003
   - False Delays: 1,132
   - Missed Delays: 260
   - True Delays: 605

2. **Probability Distribution**
   - Bimodal distribution showing model confidence
   - Clear separation between on-time and delayed classes

3. **Accuracy by Airline**
   - Performance ranges: 68-76%
   - Consistent across major carriers

4. **Overall Accuracy Pie Chart**
   - 72.2% correct predictions
   - 27.8% incorrect (mostly false positives - acceptable)

**Demo Points to Show:**
1. Open `batch_inference_results.png`
2. Explain confusion matrix interpretation
3. Show probability calibration
4. Highlight airline-specific performance

**Speaker: Rishabh (45 seconds)**
"This visualization summarizes our batch inference results. The confusion matrix shows we correctly predicted 605 delayed flights and 3,003 on-time flights. We had 260 missed delays - these are the costly errors we're working to minimize. The probability distribution shows good model calibration, and accuracy is consistent across different airlines."

---

## SLIDE 14: Future Improvements & Challenges
**What's Next?**

**Future Enhancements:**
1. **Real-Time Weather APIs** - Live weather updates instead of historical
2. **Auto-Scaling** - Handle production traffic spikes automatically
3. **A/B Testing** - Shadow deployments for safe model updates
4. **Feature Expansion** - Airport congestion, aircraft age, crew availability
5. **International Routes** - Expand beyond US domestic flights

**Technical Challenges Encountered:**
1. ✅ **Container Mismatch** - Fixed SKLearn→XGBoost deployment issue
2. ✅ **Version Compatibility** - Resolved with JSON booster format
3. ✅ **Batch Transform Speed** - Pivoted to fast real-time batch processing
4. ✅ **Feature Store Design** - Simplified from 2 groups to 1 unified

**Risks to Monitor:**
- **Data Drift:** Climate change affecting weather patterns → Hourly monitoring
- **Scalability:** Current demo setup → Production needs auto-scaling
- **Bias:** Model performance on small regional airports → Fairness metrics
- **Cost:** 24/7 endpoint ~$100/month → Scheduled scaling recommended

**Speaker: Aleena (1 minute)**
"We encountered several challenges during development. The biggest was container compatibility - we had to switch from pickle to JSON format for the XGBoost model. Another was batch processing speed, so we pivoted to using the real-time endpoint for faster results. Looking ahead, we'd add real-time weather APIs, auto-scaling for production loads, and expand to international flights. The system is production-ready but has room for enhancement."

---

## SLIDE 15: Key Achievements Summary
**What We Delivered**

✅ **Complete MLOps System:**
- Real data (5.5M records, not synthetic)
- Feature Store with 50K records
- XGBoost model meeting all targets (F1=0.358, ROC-AUC=0.663)
- Real-time endpoint with data capture
- Hourly monitoring with CloudWatch
- CI/CD pipeline with quality gates
- Batch inference with business insights

✅ **Production-Ready Components:**
- Monitoring: Automated alarms and drift detection
- Security: No PII/PHI, IAM-based access control
- Scalability: Ready for auto-scaling configuration
- Observability: Comprehensive CloudWatch dashboard
- Version Control: Model Registry with approval workflow

✅ **Business Value:**
- 72% prediction accuracy
- 251 high-risk flights identified
- Conservative approach minimizes costly missed delays
- Actionable insights for operational planning

**GitHub Repository:** https://github.com/RishabhDE/flight_delay_prediction

**Speaker: Rishabh (1 minute)**
"To summarize, we built a complete, production-ready MLOps system from end to end. It uses real data, not synthetic. All components follow AWS best practices - Feature Store, Model Registry, monitoring with alarms, and a CI/CD pipeline with quality gates. The model meets our performance targets and provides real business value by identifying high-risk flights for proactive management. All code and documentation are available in our GitHub repository."

---

## SLIDE 16: Q&A / Thank You
**Thank You!**

**Team:** FlightGuard AI
- Rishabh Malik
- Aleena Varghese

**Project Resources:**
- **GitHub:** https://github.com/RishabhDE/flight_delay_prediction
- **Data Source:** Mendeley Dataset (5.5M flight records)
- **Tech Stack:** AWS SageMaker, CloudWatch, S3, XGBoost

**Key Metrics:**
- Model: XGBoost (F1=0.358, ROC-AUC=0.663)
- Batch Accuracy: 72.16%
- Processing: 5,000 predictions in 42 seconds
- Monitoring: Hourly data quality checks

**Contact:** Available for questions!

**Speaker: Both (30 seconds)**
Rishabh: "Thank you for watching our demonstration."
Aleena: "We're happy to answer any questions about our flight delay prediction system!"

---

## TIMING BREAKDOWN (12 minutes total)
- Slide 1: Title (30 sec) - Rishabh
- Slide 2: Business Problem (1 min) - Rishabh
- Slide 3: Architecture (1 min) - Aleena
- Slide 4: Data Source (45 sec) - Aleena
- Slide 5: Feature Store (1.5 min) - Rishabh [DEMO]
- Slide 6: Model Training (1 min) - Aleena
- Slide 7: Model Registry (1 min) - Rishabh [DEMO]
- Slide 8: Endpoint (1.5 min) - Aleena [DEMO]
- Slide 9: CloudWatch (1.5 min) - Rishabh [DEMO]
- Slide 10: Monitoring Report (45 sec) - Aleena [DEMO]
- Slide 11: CI/CD Pipeline (1.5 min) - Rishabh [DEMO]
- Slide 12: Batch Inference (1 min) - Aleena
- Slide 13: Visualizations (45 sec) - Rishabh
- Slide 14: Future Work (1 min) - Aleena
- Slide 15: Summary (1 min) - Rishabh
- Slide 16: Thank You (30 sec) - Both

**Total: ~12 minutes with balanced speaking time**

---

## VIDEO RECORDING TIPS

**Before Recording:**
1. Open all AWS consoles in tabs (Feature Store, Model Registry, Endpoints, CloudWatch, Pipelines)
2. Have visualization images ready to display
3. Test screen recording and audio quality
4. Practice transitions between speakers

**During Recording:**
1. Use screen capture for AWS console demonstrations
2. Highlight/circle important metrics with cursor
3. Zoom in on key numbers and status indicators
4. Keep energy high - this shows your enthusiasm!

**Required Demonstrations (per rubric):**
✅ Feature Store and feature groups (Slide 5)
✅ Infrastructure monitoring dashboards (Slide 9)
✅ Model/data monitoring reports (Slide 10)
✅ CI/CD DAG in success AND failed state (Slide 11)
✅ Model Registry (Slide 7)
✅ Batch inference outputs (Slides 12-13)

**Good luck with your presentation! 🚀**
