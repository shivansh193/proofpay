Seed 0, 500 shoppers, 15000 visits.

| Strategy | Loss ₹/visit | Staff s/visit | Wait s/visit | Honest → Strict | Honest → Express | Fraud cash-out loss ₹ | Fraudsters caught | Median visits to catch |
|---|---|---|---|---|---|---|---|---|
| Proofpay (lower bound) | 22.5 | 72.0 | 77.0 | 28.2% | 18.1% | 155982 | 40/40 | 0.0 |
| Beta mean | 22.9 | 56.4 | 61.4 | 7.1% | 38.6% | 171143 | 40/40 | 0.0 |
| Static rules | 42.1 | 49.0 | 54.0 | 0.6% | 71.1% | 175620 | 40/40 | 0.0 |
| No trust (all Standard) | 50.3 | 53.0 | 58.0 | 0.0% | 0.0% | 581583 | 40/40 | 0.0 |

Proofpay at other score quantiles (q = 0.5 is roughly the median):

| Strategy | Loss ₹/visit | Staff s/visit | Wait s/visit | Honest → Strict | Honest → Express | Fraud cash-out loss ₹ | Fraudsters caught | Median visits to catch |
|---|---|---|---|---|---|---|---|---|
| Proofpay q = 0.02 | 23.3 | 86.9 | 91.9 | 62.3% | 6.8% | 155891 | 40/40 | 0.0 |
| Proofpay q = 0.05 | 22.8 | 79.7 | 84.7 | 45.0% | 11.5% | 155891 | 40/40 | 0.0 |
| Proofpay q = 0.1 | 22.5 | 72.0 | 77.0 | 28.2% | 18.1% | 155982 | 40/40 | 0.0 |
| Proofpay q = 0.2 | 22.7 | 63.5 | 68.5 | 14.4% | 29.1% | 163784 | 40/40 | 0.0 |
| Proofpay q = 0.35 | 22.8 | 56.8 | 61.8 | 7.8% | 40.4% | 171678 | 40/40 | 0.0 |
| Proofpay q = 0.5 | 22.8 | 53.1 | 58.1 | 5.1% | 45.8% | 174867 | 40/40 | 0.0 |
