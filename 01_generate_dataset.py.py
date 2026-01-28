import numpy as np
import pandas as pd

np.random.seed(42)

N = 5000  # تعداد ردیف‌ها

device_types = np.random.choice(
    ["camera", "thermostat", "light", "speaker"],
    size=N,
    p=[0.30, 0.25, 0.25, 0.20]
)

# برچسب حمله: حدود 35% حمله
label = np.random.choice(["Normal", "DDoS"], size=N, p=[0.65, 0.35])

# اثر نوع دستگاه روی سطح پایه ترافیک (برای اینکه ANOVA معنی‌دار شود)
device_pkt_base = {
    "camera": 120,
    "thermostat": 60,
    "light": 45,
    "speaker": 75
}
device_byte_base = {
    "camera": 90000,
    "thermostat": 25000,
    "light": 18000,
    "speaker": 35000
}

# تولید متغیرهای پیوسته
flow_pkts_s = []
flow_byts_s = []
flow_duration_s = []
avg_pkt_len = []

for dt, y in zip(device_types, label):
    base_pkt = device_pkt_base[dt]
    base_byt = device_byte_base[dt]

    if y == "Normal":
        # ترافیک عادی: متوسط و پراکندگی کمتر
        pkts = np.random.normal(loc=base_pkt, scale=20)
        byts = np.random.normal(loc=base_byt, scale=12000)
        dur = np.random.gamma(shape=2.0, scale=1.5)  # مثبت
        apl = np.random.normal(loc=650, scale=80)
    else:
        # DDoS: نرخ بسته و بایت خیلی بیشتر + پراکندگی بیشتر
        pkts = np.random.normal(loc=base_pkt * 7, scale=base_pkt * 1.8)
        byts = np.random.normal(loc=base_byt * 5, scale=base_byt * 1.6)
        dur = np.random.gamma(shape=2.5, scale=2.0)
        apl = np.random.normal(loc=520, scale=120)

    # جلوگیری از مقادیر منفی
    pkts = max(pkts, 1)
    byts = max(byts, 100)
    apl = max(apl, 60)

    flow_pkts_s.append(pkts)
    flow_byts_s.append(byts)
    flow_duration_s.append(dur)
    avg_pkt_len.append(apl)

df = pd.DataFrame({
    "label": label,
    "device_type": device_types,
    "flow_pkts_s": np.round(flow_pkts_s, 2),
    "flow_byts_s": np.round(flow_byts_s, 2),
    "flow_duration_s": np.round(flow_duration_s, 3),
    "avg_pkt_len": np.round(avg_pkt_len, 2)
})

df.to_csv("iot_ddos_synthetic.csv", index=False)

print(df.head())
print("\nSaved as iot_ddos_synthetic.csv")
print("\nCounts:\n", df["label"].value_counts())
print("\nDevice types:\n", df["device_type"].value_counts())
