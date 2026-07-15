"""
مثال تحليلي: استخراج أنماط شاذة من سجلات شبكية باستخدام Isolation Forest
هذا السكربت يعمل على بيانات تجريبية (Synthetic Data) لأغراض العرض والتوضيح.
في الاستخدام الفعلي، استبدل مصدر البيانات ببيانات القياس الناتجة عن
بيئة المحاكاة المعزولة (telemetry-data/network-logs/).
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


# ============ 1) تحميل البيانات ============
# في المشروع الفعلي: استبدل هذا بقراءة ملف سجلات حقيقي من telemetry-data/
def load_sample_data(n_normal=1000, n_anomalous=20, seed=42):
    """توليد بيانات تجريبية تحاكي سجلات اتصال شبكي (للعرض فقط)."""
    rng = np.random.default_rng(seed)

    normal = pd.DataFrame({
        "connection_duration_sec": rng.normal(5, 1.5, n_normal).clip(0.1),
        "bytes_sent": rng.normal(2000, 500, n_normal).clip(50),
        "bytes_received": rng.normal(8000, 2000, n_normal).clip(50),
        "failed_auth_attempts": rng.poisson(0.2, n_normal),
        "unique_destinations": rng.integers(1, 4, n_normal),
    })

    # نمط شاذ محتمل: عدد كبير من محاولات المصادقة الفاشلة + اتصال قصير + وجهات متعددة
    anomalous = pd.DataFrame({
        "connection_duration_sec": rng.normal(0.5, 0.2, n_anomalous).clip(0.05),
        "bytes_sent": rng.normal(300, 100, n_anomalous).clip(10),
        "bytes_received": rng.normal(150, 50, n_anomalous).clip(10),
        "failed_auth_attempts": rng.integers(15, 40, n_anomalous),
        "unique_destinations": rng.integers(10, 30, n_anomalous),
    })

    data = pd.concat([normal, anomalous], ignore_index=True)
    labels = np.array([0] * n_normal + [1] * n_anomalous)  # 1 = شاذ (للتحقق فقط)
    return data, labels


# ============ 2) هندسة الميزات ============
def preprocess(data: pd.DataFrame) -> np.ndarray:
    scaler = StandardScaler()
    return scaler.fit_transform(data)


# ============ 3) تطبيق خوارزمية كشف الشواذ ============
def detect_anomalies(features: np.ndarray, contamination: float = 0.02):
    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=42,
    )
    model.fit(features)
    scores = model.decision_function(features)   # كلما قلّت القيمة، زادت شذوذ الحالة
    predictions = model.predict(features)         # -1 = شاذ، 1 = طبيعي
    return predictions, scores


# ============ 4) تحليل النتائج واستخراج النمط ============
def summarize_pattern(data: pd.DataFrame, predictions: np.ndarray) -> pd.DataFrame:
    data = data.copy()
    data["is_anomalous"] = predictions == -1
    anomalous_records = data[data["is_anomalous"]]

    print(f"عدد الحالات الشاذة المكتشفة: {len(anomalous_records)}")
    print("\nملخص إحصائي للحالات الشاذة (لاستخراج النمط السلوكي):")
    print(anomalous_records.describe())

    return anomalous_records


# ============ التشغيل ============
if __name__ == "__main__":
    data, true_labels = load_sample_data()
    features = preprocess(data)
    predictions, scores = detect_anomalies(features)

    anomalous_records = summarize_pattern(data, predictions)

    # حفظ النتائج لاستخدامها في توثيق النمط ضمن defensive-solutions/
    anomalous_records.to_csv("detected_pattern_candidates.csv", index=False)
    print("\nتم حفظ الحالات الشاذة في: detected_pattern_candidates.csv")
    print("الخطوة التالية: راجع هذه الحالات يدوياً، ووثّق النمط في")
    print("attack-scenarios/، ثم صُغ قاعدة كشف في defensive-solutions/sigma-rules/")
