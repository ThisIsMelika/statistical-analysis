# Statistical Analysis of DDoS Attacks in IoT Network Traffic

## Overview
This project presents a comprehensive statistical analysis of network traffic
in a smart home IoT environment, with a specific focus on identifying and
characterizing Distributed Denial of Service (DDoS) attacks.

By analyzing traffic intensity metrics such as packet rate and byte rate, the
project demonstrates how classical statistical methods can be used to detect,
compare, and interpret abnormal network behavior associated with cyber attacks.

The work was developed as part of an academic course on **Statistical Methods**
and emphasizes statistical reasoning, hypothesis testing, and interpretability
over black-box machine learning models.

---

## Objectives
- Compare network traffic characteristics under **Normal** and **DDoS** conditions
- Evaluate the **statistical significance** of traffic intensity differences
- Investigate how **IoT device type** influences attack traffic behavior
- Assess the effectiveness of traffic-based features for **DDoS detection**
- Apply and interpret classical statistical tests in a real-world–inspired scenario

---

## What You Will Learn
- How to perform and interpret **descriptive statistical analysis**
- When and why to use **Welch’s t-test** instead of the standard t-test
- How to assess **normality assumptions** using the Shapiro–Wilk test
- How to compute and interpret **confidence intervals**
- How to apply **one-way ANOVA** and **Tukey HSD** post-hoc analysis
- How to use **logistic regression** for binary event prediction
- How to translate statistical outputs into **clear, real-world conclusions**

---

## Dataset
- The dataset is **synthetic** and designed to simulate realistic IoT network
  traffic under both normal operation and DDoS attack scenarios.
- It contains **5,000 network flow records** with the following key variables:

### Categorical Variables
- `label` ∈ {Normal, DDoS}
- `device_type` ∈ {camera, thermostat, light, speaker}

### Continuous Variables
- `flow_pkts_s` — Packet rate (Packets/s)
- `flow_byts_s` — Byte rate (Bytes/s)
- `flow_duration_s` — Flow duration (seconds)
- `avg_pkt_len` — Average packet length (Bytes)

> Note:  
> This dataset is intended for **educational and analytical purposes** and is
> not meant for direct deployment in real-world intrusion detection systems.

---

## Methodology
The analysis follows a structured statistical workflow:

1. **Exploratory Data Analysis**
   - Descriptive statistics
   - Data visualization (histograms, scatter plots)

2. **Assumption Checking**
   - Normality testing using the **Shapiro–Wilk test**

3. **Statistical Inference**
   - One-sample t-test
   - Two-sample **Welch t-test**
   - Confidence interval estimation

4. **Group Comparison**
   - One-way **ANOVA**
   - **Tukey HSD** post-hoc analysis

5. **Predictive Modeling**
   - **Logistic regression** for DDoS occurrence prediction
   - Interpretation using **odds ratios**

---

## Tools and Libraries
- Python
- pandas
- NumPy
- SciPy
- statsmodels
- matplotlib

---
## Repository Structure
```text
├── 01_generate_dataset.py        # Synthetic dataset generation
├── 02_statistical_analysis.py    # Main statistical analysis pipeline
├── iot_ddos_synthetic.csv        # Generated dataset
├── Stat_Project_DDoS_IoT_MelikaBagheri.pdf  # Final project report
└── README.md
```

---

## Results Summary
- Mean packet rate (`flow_pkts_s`) increased from  
  **≈ 36 Packets/s (Normal)** to **≈ 258 Packets/s (DDoS)**

- Mean byte rate (`flow_byts_s`) increased from  
  **≈ 32,509 Bytes/s (Normal)** to **≈ 179,585 Bytes/s (DDoS)**

- Welch t-tests confirmed **extremely significant differences** between Normal
  and DDoS traffic  
  (**p < 1e-300** for packet rate)

- One-way ANOVA revealed significant variation in attack intensity across IoT
  device types  
  (**F ≈ 1129, p < 1e-300**)

- Logistic regression identified **packet rate** as the strongest predictor of
  DDoS occurrence  
  (**Odds Ratio ≈ 3.26 per 10-unit increase**)

---

## How to Run

1. Clone the repository:
```bash
git clone https://github.com/ThisIsMelika/statistical-analysis.git
cd statistical-analysis
```
2.Install required dependencies:
pip install pandas numpy scipy statsmodels matplotlib

3.Run the analysis:
python 02_statistical_analysis.py

4.Statistical outputs and figures will be displayed and/or saved as defined in the script.

---

## Future Work

Validation using real-world IoT traffic datasets

Extension to machine learning–based intrusion detection models

Inclusion of temporal and protocol-level traffic features

Performance evaluation using classification metrics (ROC-AUC, F1-score)

---

## Notes

This project focuses on statistical analysis and interpretability rather
than deployment-ready intrusion detection systems.
It is intended to demonstrate strong understanding of statistical methodology,
assumption checking, and result interpretation in a cybersecurity context.

---

## Author

Melika Bagheri | 
 Statistical Methods Project – 2026




