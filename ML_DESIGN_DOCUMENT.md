# AAI-540 ML Design Document - Flight Delay Prediction System

## Team Info
- **Project Team Group #:** 5
- **Authors:** Rishabh Malik, Aleena Varghese
- **Business Name:** FlightGuard AI
- **Publication Date:** October 21, 2025

## Team Workflows
- **GitHub Project:** https://github.com/RishabhDE/flight_delay_prediction
- **Asana Board:** https://app.asana.com/1/952672460738672/project/1211392306595557/board/1211392414551839
- **Team Tracker:** https://docs.google.com/document/d/1STVH0RlqtDhpj2XyELlf0XGOgq69oD-e2eXCkeuO-5o/edit?usp=sharing

---

## 1. Problem Statement

Flight delays cost airlines billions annually and frustrate millions of passengers. Our ML system predicts whether a domestic US flight will be delayed (≥15 minutes) before departure, enabling proactive operational adjustments and passenger notifications. Using real data from 5.5M flight records (Mendeley 2023 dataset) with weather conditions, we built a binary classification model that helps airlines optimize resources and improve customer satisfaction.

## 2. Impact Measurement

Success is measured through:
- **Technical Metrics:** F1-score of 0.358 (target: ≥0.35), ROC-AUC of 0.663 (target: ≥0.65), batch inference accuracy of 72.16%
- **Business Impact:** Model conservatively predicts 34.7% delays vs actual 17.3%, minimizing missed delays (high business cost). Identifies 251 high-risk flights (>70% delay probability) for proactive passenger communication. CloudWatch monitoring with hourly checks ensures consistent performance, with alarms for error rates >10/10min and latency >1000ms.

---

## 3. Security Checklist

### Sensitive Data
- ✅ **No PII/PHI:** Only operational flight data (airline, airports, times, weather)
- ✅ **No passenger information:** No names, booking details, or demographics
- ✅ **Data Storage:** Encrypted S3 buckets with IAM role-based access
- ✅ **Endpoint Security:** VPC-enabled SageMaker endpoint (optional for production)

### Bias Concerns
- ⚠️ **Airport Representation:** Dataset may over-represent major hubs (JFK, ORD, ATL)
- ⚠️ **Seasonal Bias:** Model trained on 2023 data may not capture long-term climate changes
- ✅ **Mitigation:** Monitor prediction fairness across airlines and routes, retrain quarterly

### Ethical Considerations
- ✅ **Transparency:** Model used for operational recommendations, not automated cancellations
- ✅ **False Positives Acceptable:** Conservative predictions (over-alerting) preferred over missed delays
- ✅ **Fairness:** No discrimination based on protected classes (none in dataset)

---

## 4. Solution Overview

Complete MLOps pipeline on AWS SageMaker:
1. **Data:** Real Mendeley dataset (50K sampled from 5.5M) → Feature Store (unified feature group)
2. **Training:** 3 models tested (Logistic Regression, Random Forest, XGBoost) → XGBoost selected
3. **Deployment:** Real-time endpoint (ml.m5.large) with 100% data capture
4. **Monitoring:** Hourly baseline comparison, CloudWatch dashboard, automated alarms
5. **CI/CD:** SageMaker Pipeline with quality gates (F1≥0.35, Acc≥0.65)
6. **Inference:** Real-time endpoint + fast batch processing (5000 predictions in 42 seconds)

**Architecture:** Data Sources → Feature Store → Training → Model Registry → Quality Gate → Endpoint → Monitoring → CloudWatch

---

## 5. Data Sources

- **Source:** Mendeley "Dataset for Airline Departure Delay Prediction" (https://data.mendeley.com/datasets/xxwzw3tyfp/1)
- **Volume:** 5.5M flight records from 2023, sampled 50K for training
- **Features:** 18 airlines, 350+ airport pairs, weather conditions
- **Delay Rate:** 22.48% (realistic distribution)
- **Selection Rationale:** Real-world data, comprehensive coverage, publicly available for academic use
- **Storage:** AWS S3 (encrypted), documented in GitHub repository

---

## 6. Data Engineering

### Storage
- **S3 Bucket:** `sagemaker-us-east-1-730335352303/flight-delay-prediction/`
- **Feature Store:** Online + Offline stores for low-latency retrieval and historical training
- **Unified Design:** Single feature group (flight + weather) for simplicity

### Preprocessing
1. **Data Cleaning:** Handled missing values, removed outliers
2. **Feature Encoding:** LabelEncoder for categorical (airline, origin, destination)
3. **Scaling:** StandardScaler for numeric features (distance, temperature, wind, precipitation, visibility)
4. **Artifacts Saved:** `scaler.pkl`, `label_encoders.pkl` for consistent inference preprocessing

---

## 7. Training Data

### Data Split
- **Total:** 50,000 records
- **Training:** 70% (35,000)
- **Validation:** 15% (7,500)
- **Test:** 15% (7,500)
- **Stratification:** Maintained 22% delay rate across splits

### Labeling
- **Pre-labeled:** Dataset includes `is_delayed` column (1 = delayed ≥15min, 0 = on-time)
- **No manual labeling required**

---

## 8. Feature Engineering

### Included Features (12)
- **Flight:** airline, origin, destination, distance
- **Temporal:** day_of_week, month, departure_hour
- **Weather:** temperature, wind_speed, precipitation, visibility, snow

### Excluded Features
- **Arrival time/delay:** Would leak information (not known before departure)
- **Flight numbers:** High cardinality, not predictive
- **Passenger counts:** Not available, potential PII concerns

### Feature Importance
Top 3: distance (0.18), temperature (0.15), departure_hour (0.12)

---

## 9. Model Training & Evaluation

### Models Tested
1. **Logistic Regression:** F1=0.21, fast baseline
2. **Random Forest:** F1=0.33, good but slower
3. **XGBoost:** F1=0.358, best performance ✅ **SELECTED**

### Best Model Performance (XGBoost)
- **Accuracy:** 66.59%
- **Precision:** 26.82%
- **Recall:** 53.99%
- **F1-Score:** 0.358 ✅ (meets ≥0.35 target)
- **ROC-AUC:** 0.663 ✅ (meets ≥0.65 target)

### Training Configuration
- **Framework:** XGBoost 1.7 in SageMaker container
- **Instance:** ml.m5.xlarge
- **Hyperparameters:** max_depth=6, eta=0.1, objective=binary:logistic
- **Training Time:** ~5 minutes

---

## 10. Model Deployment

### Endpoint Configuration
- **Name:** `flight-delay-predictor-2025-10-21-06-04-56`
- **Instance:** ml.m5.large (cost-effective for demo, scalable for production)
- **Model Format:** XGBoost JSON booster (avoids version compatibility issues)
- **Data Capture:** 100% sampling to S3 for monitoring

### Deployment Challenges Solved
1. **Container Mismatch:** Fixed SKLearn→XGBoost container issue
2. **Version Compatibility:** Used JSON booster format instead of pickle
3. **Serialization:** Converted numpy types to Python floats for JSON output
4. **Feature Names:** Added explicit feature_names to DMatrix

### Inference Format
- **Input:** JSON with 12 features
- **Output:** JSON with prediction (0/1) and probabilities [on-time, delay]
- **Latency:** <100ms per prediction

---

## 11. Model Monitoring

### Monitoring Schedule
- **Name:** `flight-delay-monitor-2025-10-21-06-25-01`
- **Frequency:** Hourly baseline comparison
- **Baseline:** 5,000 records with statistics and constraints

### CloudWatch Dashboard
- **Name:** `FlightDelayPrediction-ModelMonitoring`
- **Metrics:** Invocations, errors, latency, model latency, 4xx/5xx errors
- **Alarms:** 
  - High error rate (>10 errors per 10 minutes)
  - High latency (>1000ms)

### Monitoring Reports
- **Location:** `s3://.../monitoring/reports/`
- **Data Drift Detection:** Compares feature distributions hourly
- **Automated Alerts:** SNS notifications on violations

---

## 12. CI/CD Pipeline

### SageMaker Pipeline
- **Name:** `FlightDelayPredictionPipeline`
- **Steps:**
  1. **Preprocessing:** Feature engineering and data validation
  2. **Training:** XGBoost model training
  3. **Evaluation:** Calculate metrics (F1, accuracy, ROC-AUC)
  4. **Quality Gate:** Conditional deployment if F1≥0.35 AND accuracy≥0.65
  5. **Register Model:** Add to Model Registry with approval workflow
  6. **Fail Step:** Terminate if quality thresholds not met

### Execution Results
- **Pass Scenario:** Model met all quality gates → Deployed successfully
- **Fail Scenario:** Tested with degraded model → Pipeline stopped at quality gate ✅
- **Model Registry:** Models versioned in `FlightDelayPredictionPackageGroup`

---

## 13. Batch Inference

### Implementation
- **Approach:** Real-time endpoint with batch processing (faster for demo than Batch Transform)
- **Performance:** 5,000 predictions in 42 seconds
- **Accuracy:** 72.16% (better than real-time test due to different data distribution)
- **ROC-AUC:** 78.13%

### Business Insights
- **High-Risk Flights:** 251 flights (5%) with >70% delay probability
- **Conservative Model:** Predicts 34.7% delays vs actual 17.3%
- **Airline Variations:** Prediction accuracy ranges 68-76% across airlines
- **Use Case:** Daily operational planning, proactive passenger notifications

---

## 14. Future Improvements

1. **Real-Time Weather Integration:** Connect to live weather APIs for up-to-the-minute conditions
2. **Auto-Scaling:** Configure endpoint auto-scaling for production traffic
3. **A/B Testing:** Deploy shadow models to compare new versions safely
4. **Feature Expansion:** Add airport congestion, aircraft age, crew availability
5. **International Flights:** Expand beyond US domestic routes

---

## 15. Risks & Challenges

### Technical Risks
- **Data Drift:** Weather patterns changing due to climate change → Mitigated by hourly monitoring
- **Scalability:** Current endpoint for demo load → Use auto-scaling and batch transform for millions of flights
- **Model Staleness:** 2023 data may not reflect 2025 patterns → Implement quarterly retraining

### Ethical Risks
- **Over-Reliance:** Airlines must not use predictions for automated cancellations without human review
- **Bias:** Model may perform differently across small regional airports → Monitor fairness metrics

### Operational Risks
- **Cost:** Continuous endpoint costs ~$100/month → Use scheduled scaling or batch-only approach
- **Dependencies:** S3/SageMaker outages impact predictions → Implement fallback rules

---

## 16. Conclusion

We delivered a complete, production-ready ML system for flight delay prediction using AWS SageMaker MLOps best practices. The system uses real data (not synthetic), meets all performance targets (F1=0.358, ROC-AUC=0.663), and includes comprehensive monitoring with hourly checks and CloudWatch alarms. The CI/CD pipeline ensures quality gates prevent degraded models from deploying. Batch inference demonstrates practical business value with 72% accuracy identifying high-risk flights for proactive passenger communication.

**Key Achievements:**
- ✅ Real Mendeley dataset (5.5M records)
- ✅ Deployed XGBoost model meeting all targets
- ✅ Feature Store with unified design
- ✅ Hourly monitoring with CloudWatch
- ✅ CI/CD pipeline with quality gates
- ✅ Fast batch inference (42 seconds for 5K predictions)
- ✅ Complete GitHub repository with 5 notebooks

**GitHub Repository:** https://github.com/RishabhDE/flight_delay_prediction
