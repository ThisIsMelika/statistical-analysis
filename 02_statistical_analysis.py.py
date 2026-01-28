# =========================================
# Project: Statistical Analysis of DDoS in IoT (Synthetic Dataset)
# Author: (Your name)
# Requirements:
#   pip install pandas numpy scipy statsmodels matplotlib
# =========================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# -----------------------------
# 0) CONFIG
# -----------------------------
DATA_PATH = "iot_ddos_synthetic.csv"   # مسیر فایل CSV
OUT_DIR = "outputs"
ALPHA = 0.05
CI_LEVEL = 0.95

# ستون‌ها
LABEL_COL = "label"          # Normal / DDoS
DEVICE_COL = "device_type"   # camera / thermostat / light / speaker
CONT_COLS = ["flow_pkts_s", "flow_byts_s", "flow_duration_s", "avg_pkt_len"]

# -----------------------------
# 1) Helpers
# -----------------------------
def ensure_outdir(path):
    os.makedirs(path, exist_ok=True)

def mean_ci(x, conf=0.95):
    x = np.array(pd.Series(x).dropna())
    n = len(x)
    m = x.mean()
    se = stats.sem(x)
    tcrit = stats.t.ppf((1 + conf) / 2, df=n - 1)
    return m, (m - tcrit * se, m + tcrit * se), n

def welch_ttest_ci(x1, x2, conf=0.95):
    x1 = np.array(pd.Series(x1).dropna())
    x2 = np.array(pd.Series(x2).dropna())

    t_stat, p_val = stats.ttest_ind(x1, x2, equal_var=False)

    mean_diff = x1.mean() - x2.mean()
    se = np.sqrt(x1.var(ddof=1)/len(x1) + x2.var(ddof=1)/len(x2))

    # Welch-Satterthwaite df
    df_w = (x1.var(ddof=1)/len(x1) + x2.var(ddof=1)/len(x2))**2 / \
           ((x1.var(ddof=1)/len(x1))**2/(len(x1)-1) + (x2.var(ddof=1)/len(x2))**2/(len(x2)-1))

    tcrit = stats.t.ppf((1 + conf)/2, df=df_w)
    ci = (mean_diff - tcrit*se, mean_diff + tcrit*se)

    return t_stat, p_val, mean_diff, ci, df_w

def shapiro_test(x, max_n=5000, seed=42):
    x = pd.Series(x).dropna()
    if len(x) > max_n:
        x = x.sample(max_n, random_state=seed)
    w, p = stats.shapiro(x)
    return w, p, len(x)

def save_hist(x, title, filename):
    plt.figure()
    plt.hist(pd.Series(x).dropna(), bins=30)
    plt.title(title)
    plt.xlabel(title)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(filename, dpi=160)
    plt.close()

# -----------------------------
# 2) Load data
# -----------------------------
ensure_outdir(OUT_DIR)
df = pd.read_csv(DATA_PATH).dropna().copy()

# -----------------------------
# 3) Basic info / descriptive stats
# -----------------------------
info_lines = []
info_lines.append(f"Rows: {df.shape[0]}, Cols: {df.shape[1]}\n")
info_lines.append("Label counts:\n" + str(df[LABEL_COL].value_counts()) + "\n")
info_lines.append("Device counts:\n" + str(df[DEVICE_COL].value_counts()) + "\n")

desc_all = df[CONT_COLS].describe().T
desc_by_label = df.groupby(LABEL_COL)[CONT_COLS].agg(["count","mean","std","min","median","max"])

info_lines.append("\nDescriptive (All):\n" + desc_all.to_string() + "\n")
info_lines.append("\nDescriptive (By label):\n" + desc_by_label.to_string() + "\n")

# -----------------------------
# 4) Normality tests (Shapiro) + histograms
# -----------------------------
shapiro_rows = []
for col in CONT_COLS:
    w, p, n = shapiro_test(df[col])
    shapiro_rows.append(("All", col, n, w, p))

for lbl, grp in df.groupby(LABEL_COL):
    for col in CONT_COLS:
        w, p, n = shapiro_test(grp[col])
        shapiro_rows.append((lbl, col, n, w, p))

shapiro_df = pd.DataFrame(shapiro_rows, columns=["group","variable","n_used","W","p_value"])
info_lines.append("\nShapiro normality tests:\n" + shapiro_df.to_string(index=False) + "\n")

# Save some histograms
for col in CONT_COLS:
    save_hist(df[col], f"Histogram: {col}", os.path.join(OUT_DIR, f"hist_{col}.png"))

# -----------------------------
# 5) Confidence Interval (example): mean of flow_pkts_s in DDoS
# -----------------------------
ddos = df[df[LABEL_COL] == "DDoS"]
normal = df[df[LABEL_COL] == "Normal"]

m, ci, n = mean_ci(ddos["flow_pkts_s"], CI_LEVEL)
info_lines.append(f"\nCI({int(CI_LEVEL*100)}%) for mean flow_pkts_s in DDoS: mean={m:.4f}, CI=({ci[0]:.4f},{ci[1]:.4f}), n={n}\n")

# -----------------------------
# 6) One-sample hypothesis test (example): Normal mean flow_pkts_s = 75?
# H0: mu = 75, H1: mu != 75
# -----------------------------
mu0 = 75.0
t_stat, p_val = stats.ttest_1samp(normal["flow_pkts_s"], popmean=mu0)
info_lines.append("\nOne-sample t-test (Normal traffic):\n")
info_lines.append(f"H0: mean(flow_pkts_s) = {mu0}\n")
info_lines.append(f"t={t_stat:.6f}, p-value={p_val:.12g}\n")
info_lines.append("Decision: " + ("Reject H0\n" if p_val < ALPHA else "Fail to reject H0\n"))

# -----------------------------
# 7) Two-sample test (Welch): DDoS vs Normal for pkts and bytes
# -----------------------------
t1, p1, diff1, ci1, dfw1 = welch_ttest_ci(ddos["flow_pkts_s"], normal["flow_pkts_s"], CI_LEVEL)
t2, p2, diff2, ci2, dfw2 = welch_ttest_ci(ddos["flow_byts_s"], normal["flow_byts_s"], CI_LEVEL)

info_lines.append("\nWelch two-sample t-test: DDoS vs Normal\n")

def pformat(p):
    return "< 1e-300" if (p == 0.0) else f"{p:.12g}"

info_lines.append(f"[flow_pkts_s] t={t1:.6f}, p={pformat(p1)}, mean_diff(DDoS-Normal)={diff1:.4f}, CI=({ci1[0]:.4f},{ci1[1]:.4f}), df~{dfw1:.2f}\n")
info_lines.append(f"[flow_byts_s] t={t2:.6f}, p={pformat(p2)}, mean_diff(DDoS-Normal)={diff2:.4f}, CI=({ci2[0]:.4f},{ci2[1]:.4f}), df~{dfw2:.2f}\n")

# -----------------------------
# 8) ANOVA (One-way): compare flow_pkts_s across device types in DDoS
# -----------------------------
groups = [g["flow_pkts_s"].values for _, g in ddos.groupby(DEVICE_COL)]
f_stat, p_anova = stats.f_oneway(*groups)

ddos_means = ddos.groupby(DEVICE_COL)["flow_pkts_s"].agg(["count","mean","std"])
info_lines.append("\nOne-way ANOVA (DDoS only): flow_pkts_s across device_type\n")
info_lines.append("Group means:\n" + ddos_means.to_string() + "\n")
info_lines.append(f"F={f_stat:.6f}, p={pformat(p_anova)}\n")
info_lines.append("Decision: " + ("Reject H0 (means not all equal)\n" if p_anova < ALPHA else "Fail to reject H0\n"))

# Tukey post-hoc
tukey = pairwise_tukeyhsd(endog=ddos["flow_pkts_s"], groups=ddos[DEVICE_COL], alpha=ALPHA)
info_lines.append("\nTukey HSD (post-hoc):\n" + str(tukey) + "\n")

# -----------------------------
# 9) Regression: Logistic (predict DDoS)
# is_ddos ~ flow_pkts_s + avg_pkt_len + device_type
# -----------------------------
df["is_ddos"] = (df[LABEL_COL] == "DDoS").astype(int)
logit = smf.logit("is_ddos ~ flow_pkts_s + avg_pkt_len + C(device_type)", data=df).fit(disp=False)

info_lines.append("\nLogistic Regression:\n")
info_lines.append(str(logit.summary()) + "\n")

# Odds ratio for +10 packets/s
beta = logit.params["flow_pkts_s"]
or10 = float(np.exp(beta * 10))
info_lines.append(f"Odds ratio for +10 in flow_pkts_s: OR10={or10:.4f}\n")

# -----------------------------
# 10) Save results to file
# -----------------------------
with open(os.path.join(OUT_DIR, "results.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(info_lines))

print("Done. Outputs saved in:", OUT_DIR)
print("Key file:", os.path.join(OUT_DIR, "results.txt"))
