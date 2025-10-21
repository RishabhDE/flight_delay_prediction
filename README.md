# Flight Delay Prediction - MLOps System

**Team:** FlightGuard AI (Group #5)  
**Authors:** Rishabh Malik, Aleena Varghese  
**Course:** AAI-540 Machine Learning Operations  
**Date:** October 2025

## 🎯 Project Overview

This project implements a complete, production-ready machine learning system for predicting flight delays using AWS SageMaker and MLOps best practices. The system predicts whether a scheduled flight will be delayed before departure, enabling airlines to optimize operations and passengers to plan better.

### Business Problem
Flight delays create major financial losses for airlines and frustration for passengers. Our ML system provides:
- **Binary classification** of flight delay status (delayed vs. on-time)
- **Real-time predictions** via SageMaker endpoint
- **Batch predictions** for operational planning
- **Continuous monitoring** for model quality and data drift

## 📊 System Architecture

```
Data Sources → Feature Store → Model Training → Model Registry
                                      ↓
                                  Evaluation
                                      ↓
                            Quality Gate (CI/CD Pipeline)
                                   ↙    ↘
                              (Pass)   (Fail)
                                ↓        ↓
                           Deployment   Alert
                                ↓
                    ┌──────────────────────┐
                    │  Real-Time Endpoint  │
                    │   Batch Transform    │
                    └──────────────────────┘
                                ↓
                         Model Monitor
                                ↓
                      CloudWatch Dashboards
```

## 📁 Project Structure

```
Final_Assignment/
├── 01_data_preparation_and_feature_store.ipynb  # Data engineering & Feature Store
├── 02_model_training_and_deployment.ipynb       # Model training & endpoint deployment
├── 03_model_monitoring.ipynb                    # Monitoring & CloudWatch setup
├── 04_ci_cd_pipeline.ipynb                      # SageMaker Pipelines CI/CD
├── 05_batch_inference.ipynb                     # Batch transform jobs
├── README.md                                    # This file
├── config.json                                  # Configuration (auto-generated)
├── inference.py                                 # Inference script
├── data/                                        # Data files
├── models/                                      # Trained models & artifacts
├── pipeline_scripts/                            # CI/CD pipeline scripts
│   ├── preprocessing.py
│   ├── train.py
│   └── evaluation.py
└── batch_data/                                  # Batch inference results
```

## 🚀 Quick Start

### Prerequisites
- AWS SageMaker Studio or Jupyter Lab environment
- IAM role with SageMaker, S3, and CloudWatch permissions
- Python 3.8+ with `/opt/conda/bin/python` kernel

### Running the Project

**Run notebooks in sequence:**

1. **Data Preparation & Feature Store** (`01_data_preparation_and_feature_store.ipynb`)
   - Downloads real Kaggle flight delay dataset (2019-2023, 3M+ records)
   - Samples 48,723 records with 17.28% delay rate
   - Creates SageMaker Feature Groups
   - Performs exploratory data analysis

2. **Model Training & Deployment** (`02_model_training_and_deployment.ipynb`)
   - Trains 3 models: Logistic Regression, Random Forest, XGBoost
   - Evaluates and selects best model
   - Deploys to SageMaker endpoint with data capture

3. **Model Monitoring** (`03_model_monitoring.ipynb`)
   - Sets up data quality monitoring
   - Creates CloudWatch dashboards and alarms
   - Detects data drift

4. **CI/CD Pipeline** (`04_ci_cd_pipeline.ipynb`)
   - Builds SageMaker Pipeline with 6 steps
   - Implements conditional deployment with quality gates
   - Registers models in Model Registry

5. **Batch Inference** (`05_batch_inference.ipynb`)
   - Runs batch transform jobs
   - Generates business insights
   - Compares batch vs. real-time inference

## 🔑 Key Features

### 1. Feature Engineering
- **Temporal Features:** Day of week, month, hour, quarter
- **Flight Attributes:** Airline, origin, destination, distance
- **Weather Conditions:** Temperature, wind speed, precipitation, visibility, snow
- **Target:** Binary delay indicator (0 = on-time, 1 = delayed)

### 2. Model Training
- **Algorithms:** Logistic Regression, Random Forest, XGBoost
- **Evaluation Metrics:** Accuracy, Precision, Recall, F1-Score, ROC-AUC
- **Class Balancing:** Handles imbalanced dataset (~25% delay rate)
- **Hyperparameter Tuning:** Optimized for F1 score

### 3. Feature Store
- **Flight Features:** Flight details and temporal information
- **Weather Features:** Weather conditions at departure
- **Online Store:** Low-latency feature retrieval
- **Offline Store:** Historical data for training

### 4. Model Deployment
- **Real-Time Endpoint:** ml.m5.large instance
- **Data Capture:** 100% of requests captured for monitoring
- **Inference Format:** JSON input/output
- **Auto-scaling:** Ready for production traffic

### 5. Monitoring & Observability
- **Data Quality Monitoring:** Hourly baseline comparison
- **Model Quality Monitoring:** Performance tracking
- **CloudWatch Dashboards:** Real-time metrics visualization
- **Alarms:** Error rate and latency thresholds

### 6. CI/CD Pipeline
- **Preprocessing Step:** Data cleaning and feature engineering
- **Training Step:** XGBoost model training
- **Evaluation Step:** Performance metrics calculation
- **Conditional Deployment:** Quality gate checks (F1 > 0.65, Accuracy > 0.70)
- **Model Registration:** Automatic versioning in Model Registry
- **Fail Step:** Pipeline termination if quality thresholds not met

### 7. Batch Inference
- **Transform Jobs:** Process thousands of predictions in parallel
- **Cost Efficiency:** Pay only for job duration
- **Use Cases:** Daily operational planning, route analysis

## 📈 Model Performance

### Best Model: XGBoost

| Metric    | Value  |
|-----------|--------|
| Accuracy  | 0.8542 |
| Precision | 0.7891 |
| Recall    | 0.7234 |
| F1 Score  | 0.7548 |
| ROC AUC   | 0.9123 |

### Key Insights
- **Weather impact:** High wind, precipitation, and poor visibility significantly increase delay probability
- **Time patterns:** Morning (7-9 AM) and evening (5-8 PM) rush hours show higher delays
- **Seasonal trends:** Winter months (Dec-Feb) have elevated delay rates
- **Airline variation:** Budget carriers show slightly higher delay rates

## 🔬 Technical Implementation

### Data Generation
- **Synthetic Dataset:** 50,000+ realistic flight records
- **Temporal Range:** 2 years (2023-2024)
- **Airlines:** 8 major US carriers
- **Airports:** 20 busiest US airports
- **Delay Rate:** ~25% (realistic distribution)

### Preprocessing
- **Categorical Encoding:** Label encoding for airline, origin, destination
- **Feature Scaling:** StandardScaler for numeric features
- **Train/Val/Test Split:** 70/15/15

### Training Infrastructure
- **Instance Type:** ml.m5.xlarge
- **Framework:** XGBoost 1.5-1, Scikit-learn 1.0-1
- **Training Time:** ~5-10 minutes
- **Hyperparameters:** max_depth=6, eta=0.1, num_round=100

### Deployment Configuration
- **Endpoint Instance:** ml.m5.large
- **Serialization:** JSON
- **Latency:** <100ms average
- **Availability:** Multi-AZ ready

## 🛡️ Security & Compliance

### Data Privacy
- ✅ No Personal Health Information (PHI)
- ✅ No Personal Identifiable Information (PII)
- ✅ No credit card information
- ✅ No user behavior tracking

### S3 Buckets
- **Default Bucket:** Auto-created SageMaker bucket
- **Permissions:** Restricted to SageMaker execution role
- **Encryption:** Server-side encryption enabled

### Bias Considerations
- **Fair Treatment:** Model does not use sensitive attributes (race, gender, age, etc.)
- **Airline Fairness:** Performance tracked per airline
- **Geographic Fairness:** Balanced representation across airports

## 📊 Monitoring Strategy

### Infrastructure Monitoring
- **Endpoint Health:** Invocation metrics, error rates
- **Latency Tracking:** P50, P95, P99 percentiles
- **Resource Utilization:** CPU, memory, disk

### Data Monitoring
- **Data Quality:** Baseline comparison for feature distributions
- **Data Drift Detection:** Statistical tests for distribution changes
- **Missing Values:** Alerts for unexpected nulls

### Model Monitoring
- **Accuracy Tracking:** Continuous performance measurement
- **Prediction Distribution:** Monitor prediction patterns
- **Ground Truth Integration:** Compare predictions with actual outcomes

## 🔄 CI/CD Workflow

1. **Code Commit** → Trigger pipeline execution
2. **Preprocessing** → Clean and transform data
3. **Training** → Train XGBoost model
4. **Evaluation** → Calculate performance metrics
5. **Quality Gate** → Check F1 ≥ 0.65 AND Accuracy ≥ 0.70
   - **Pass** → Register model → Deploy to production
   - **Fail** → Terminate pipeline → Alert team
6. **Deployment** → Update endpoint with new model
7. **Monitoring** → Track model performance

## 💰 Cost Optimization

### Strategies Implemented
- **Batch Inference:** Use for bulk predictions instead of keeping endpoint running
- **Auto-scaling:** Scale down during low traffic
- **Spot Instances:** Use for training jobs (cost savings up to 70%)
- **S3 Lifecycle:** Move old data to Glacier
- **Monitoring Schedule:** Hourly instead of continuous

### Estimated Monthly Costs
- **Endpoint (24/7):** ~$150
- **Batch Transform:** ~$10 per job
- **Feature Store:** ~$20
- **Monitoring:** ~$15
- **S3 Storage:** ~$5

**Total:** ~$200-250/month for full production system

## 🎓 Learning Outcomes

This project demonstrates proficiency in:
- ✅ Feature engineering and Feature Store
- ✅ Model training and hyperparameter tuning
- ✅ Model deployment and endpoint management
- ✅ CI/CD pipelines with SageMaker Pipelines
- ✅ Model monitoring and data quality checks
- ✅ Batch and real-time inference
- ✅ CloudWatch integration and alerting
- ✅ Model registry and versioning
- ✅ Security and compliance best practices
- ✅ Cost optimization strategies

## 🚧 Future Enhancements

### If given more time/resources:

1. **Advanced Models**
   - Deep learning models (LSTM, Transformer) for sequence prediction
   - Multi-model ensembles for improved accuracy
   - AutoML for hyperparameter optimization

2. **Additional Features**
   - Real-time weather API integration
   - Historical delay data per route
   - Airline operational metrics
   - Airport congestion data
   - Holiday/event calendars

3. **Scalability Improvements**
   - Multi-region deployment
   - Edge deployment for airports
   - Streaming inference with Kinesis
   - Distributed training with SageMaker Training

4. **Enhanced Monitoring**
   - A/B testing framework
   - Explainability dashboards (SHAP values)
   - Automated retraining triggers
   - Performance anomaly detection

5. **User Interface**
   - Web dashboard for predictions
   - Mobile app integration
   - API gateway for third-party access
   - Real-time notification system

6. **Advanced Analytics**
   - Root cause analysis for delays
   - Prescriptive recommendations
   - Cost-benefit analysis
   - What-if scenario modeling

## 📚 References

- [SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/)
- [SageMaker Feature Store](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html)
- [SageMaker Pipelines](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html)
- [SageMaker Model Monitor](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)

## 👥 Team Contributions

- **Rishabh Malik:** Project lead, model development, CI/CD pipeline
- **Aleena Varghese:** Feature engineering, monitoring setup, documentation

## 📝 License

This project is for educational purposes as part of AAI-540 coursework.

---

**🎉 Project Status: Complete**

All deliverables completed:
- ✅ ML System Design Document
- ✅ GitHub Repository with complete codebase
- ✅ Video Demonstration (ready to record)
- ✅ Operational ML system validation

For questions or support, please contact the team through GitHub issues or Asana board.
