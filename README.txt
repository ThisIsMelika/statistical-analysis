# Statistical Analysis of DDoS Attacks in IoT Network Traffic

This project investigates the relationship between network traffic intensity
(Packets per second and Bytes per second) and the occurrence of Distributed
Denial of Service (DDoS) attacks in Internet of Things (IoT) devices within a
smart home environment.

The analysis applies statistical methods to compare normal and attack traffic,
evaluate differences across device types, and assess the predictive power of
traffic-related features for DDoS detection.

## Objectives
- Analyze and compare network traffic characteristics under normal and DDoS conditions
- Evaluate statistical significance of traffic intensity differences
- Examine the impact of IoT device type on attack traffic behavior
- Assess the suitability of traffic intensity metrics for DDoS attack detection

## Methodology
- Descriptive statistics and data visualization
- Normality testing (Shapiro–Wilk)
- Hypothesis testing:
  - One-sample t-test
  - Two-sample Welch t-test
  - One-way ANOVA with Tukey HSD post-hoc analysis
- Logistic regression for DDoS occurrence prediction

## Dataset
The dataset used in this project is **synthetic** and was generated to simulate
realistic IoT network traffic under normal operation and DDoS attack scenarios.
It is intended for educational and analytical purposes rather than direct
deployment in real-world systems.

## Tools and Libraries
- Python
- pandas
- scipy
- statsmodels
- matplotlib

## Files
- `Stat_Project_DDoS_IoT_MelikaBagheri.pdf` — Final statistical report
- `ddos_iot_stat_analysis.py` — Python source code for data analysis
- `iot_ddos_synthetic.csv` — Synthetic dataset used in the analysis

## Results Summary
- Mean packet rate (`flow_pkts_s`) increased from **≈ 36 Packets/s** (Normal)
  to **≈ 258 Packets/s** during DDoS attacks
- Mean byte rate (`flow_byts_s`) increased from **≈ 32,509 Bytes/s** (Normal)
  to **≈ 179,585 Bytes/s** during DDoS attacks
- Welch t-tests confirmed highly significant differences between Normal and
  DDoS traffic (**p < 1e-300** for packet rate)
- One-way ANOVA showed significant variation in attack traffic intensity across
  IoT device types (**F ≈ 1129, p < 1e-300**)
- Logistic regression identified packet rate as the strongest predictor of DDoS
  occurrence (Odds Ratio ≈ **3.26** per 10-unit increase)

## How to Run

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
2.	Install required dependencies:
    python ddos_iot_stat_analysis.py
3.	Run the analysis script:
    python ddos_iot_stat_analysis.py
4.	Generated figures and statistical outputs will be displayed or saved as
defined in the script.

##Future Work

	•	Validation of results using real-world IoT network traffic datasets
	•	Application of machine learning models for automated DDoS detection
	•	Expansion of feature space using temporal, flow-based, and protocol-level metrics
	•	Performance evaluation using classification metrics such as ROC-AUC and F1-score

##Notes

This project was developed as part of an academic statistics course and focuses
on statistical analysis rather than deployment-ready intrusion detection systems.
