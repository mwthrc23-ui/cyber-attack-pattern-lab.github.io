# مستودع محاكاة الهجمات السيبرانية واستخراج الأنماط الدفاعية

## نظرة عامة
هذا المستودع مشروع بحثي دفاعي يهدف إلى محاكاة سلوكيات الهجمات السيبرانية داخل بيئات
معزولة تماماً، بغرض جمع بيانات سلوكية دقيقة وتحليلها باستخدام تقنيات التعلم الآلي
وكشف الشواذ لاستخراج أنماط هجومية جديدة، ثم ترجمة هذه الأنماط إلى قواعد وحلول وقائية
عملية. المشروع لا يحتوي على أي أدوات استغلالية جاهزة أو أكواد هجومية، ويعتمد كلياً على
أدوات محاكاة معتمدة ومصنفة أمنياً مثل MITRE ATT&CK, MITRE Caldera, Atomic Red Team.

## سياسة الاستخدام
راجع ملف `ETHICS_POLICY.md` قبل أي استخدام. الاستخدام يقتصر على بيئات الاختبار
المعزولة وبإذن كتابي فقط.

## هيكل المستودع

```
cyber-attack-pattern-lab/
├── README.md
├── LICENSE
├── ETHICS_POLICY.md
├── .gitignore
│
├── lab-environments/
│   ├── docker-compose.yml
│   └── network-topology-diagrams/
│       └── README.md
│
├── attack-scenarios/
│   ├── scenario-template.md
│   ├── initial-access/
│   ├── lateral-movement/
│   ├── privilege-escalation/
│   └── exfiltration/
│
├── telemetry-data/
│   ├── network-logs/
│   ├── endpoint-logs/
│   └── siem-exports/
│
├── pattern-extraction/
│   ├── notebooks/
│   │   └── anomaly_detection_example.py
│   └── requirements.txt
│
├── defensive-solutions/
│   ├── sigma-rules/
│   │   └── example_lateral_movement.yml
│   ├── suricata-rules/
│   └── mitigation-playbooks/
│       └── template.md
│
└── docs/
    ├── methodology.md
    └── contribution-guidelines.md
```

## طريقة التشغيل السريعة
1. ثبّت Docker و Docker Compose.
2. انتقل إلى `lab-environments/` وشغّل: `docker compose up -d`
3. راجع `attack-scenarios/scenario-template.md` لإنشاء سيناريو محاكاة جديد.
4. ثبّت متطلبات التحليل: `pip install -r pattern-extraction/requirements.txt`
5. شغّل نموذج التحليل: `python pattern-extraction/notebooks/anomaly_detection_example.py`

## الأدوات الموصى بها
- محاكاة: MITRE Caldera, Atomic Red Team
- جمع بيانات: Wazuh, Zeek, Suricata
- تحليل: scikit-learn, PyOD, pandas
- كشف: Sigma rules, Suricata rules

## الترخيص
MIT License مع شرط الالتزام بسياسة الاستخدام الأخلاقي في `ETHICS_POLICY.md`.

## المساهمة
راجع `docs/contribution-guidelines.md` قبل تقديم أي Pull Request.
