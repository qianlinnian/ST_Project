# 实验对比报告

| 测试项目 | LLM | 模型 | 用例数 | 耗时 | 语句覆盖 | 分支覆盖 | 轮次 | 通过/失败 | 时间 |
|----------|-----|------|--------|------|----------|----------|------|-----------|------|
| convert_number_to_words.py | deepseek-chat | deepseek-chat | 28 | 113.9s | 91.0% | 92.3% | 3 | 18/8 | 2026-03-22 16:24:51 |
| convert_number_to_words.py | deepseek-reasoner | deepseek-reasoner | 28 | 483.8s | 91.0% | 92.3% | 3 | 16/11 | 2026-03-22 16:32:55 |
| convert_number_to_words.py | google | gemini-2.5-flash | 44 | 151.4s | 91.0% | 92.3% | 3 | 39/4 | 2026-03-22 16:35:26 |
| convert_number_to_words.py | github | gpt-4o-mini | 27 | 29.7s | 91.0% | 92.3% | 3 | 17/7 | 2026-03-22 16:35:56 |
| index.js | deepseek-chat | deepseek-chat | 96 | 335.8s | 26.9% | 19.8% | 3 | 0/96 | 2026-03-22 17:12:44 |
| index.js | deepseek-reasoner | deepseek-reasoner | 40 | 428.0s | 43.3% | 32.4% | 3 | 0/40 | 2026-03-22 17:19:52 |
| index.js | google | gemini-2.5-flash | 280 | 464.2s | 58.4% | 44.0% | 3 | 1/279 | 2026-03-22 17:27:36 |
| index.js | github | gpt-4o-mini | 31 | 56.4s | 26.5% | 18.7% | 3 | 0/31 | 2026-03-22 17:28:33 |
| index.js | deepseek-chat | deepseek-chat | 66 | 350.9s | 38.2% | 28.6% | 3 | 7/59 | 2026-03-22 17:56:17 |
| index.js | deepseek-reasoner | deepseek-reasoner | 98 | 670.3s | 66.4% | 51.1% | 3 | 4/94 | 2026-03-22 18:07:28 |
| index.js | google | gemini-2.5-flash | 372 | 534.9s | 31.1% | 18.1% | 3 | 0/372 | 2026-03-22 18:16:23 |
| index.js | github | gpt-4o-mini | 26 | 46.9s | 26.9% | 19.8% | 3 | 0/26 | 2026-03-22 18:17:09 |
| convert_number_to_words.py | deepseek-chat | deepseek-chat | 29 | 105.0s | 91.0% | 92.3% | 3 | 22/5 | 2026-03-22 18:26:04 |
| convert_number_to_words.py | deepseek-reasoner | deepseek-reasoner | 33 | 740.0s | 91.0% | 92.3% | 3 | 27/4 | 2026-03-22 18:38:24 |
| convert_number_to_words.py | google | gemini-2.5-flash | 38 | 189.7s | 91.0% | 92.3% | 3 | 33/4 | 2026-03-22 18:41:34 |
| convert_number_to_words.py | github | gpt-4o-mini | 18 | 24.2s | 85.9% | 84.6% | 3 | 8/7 | 2026-03-22 18:41:58 |
| index.js | deepseek-chat | deepseek-chat | 84 | 320.1s | 38.2% | 28.6% | 3 | 0/84 | 2026-03-22 18:47:23 |
| index.js | deepseek-reasoner | deepseek-reasoner | 105 | 543.5s | 28.1% | 20.3% | 3 | 0/105 | 2026-03-22 18:56:26 |
| index.js | github | gpt-4o-mini | 30 | 53.8s | 26.9% | 19.2% | 3 | 0/30 | 2026-03-22 19:01:30 |
| convert_number_to_words.py | deepseek-chat | deepseek-chat | 22 | 90.5s | 91.0% | 92.3% | 1 | 21/1 | 2026-03-22 22:34:27 |
| convert_number_to_words.py | deepseek-reasoner | deepseek-reasoner | 20 | 259.7s | 91.0% | 92.3% | 1 | 19/1 | 2026-03-22 22:38:47 |
| convert_number_to_words.py | github | gpt-4o-mini | 15 | 21.4s | 91.0% | 92.3% | 1 | 13/2 | 2026-03-22 22:54:04 |
| convert_number_to_words.py | deepseek-chat | deepseek-chat | 18 | 94.0s | 91.0% | 92.3% | 1 | 17/1 | 2026-03-22 22:58:11 |
| convert_number_to_words.py | deepseek-reasoner | deepseek-reasoner | 23 | 271.5s | 91.0% | 92.3% | 1 | 20/3 | 2026-03-22 23:02:43 |
| convert_number_to_words.py | google | gemini-2.5-flash | 26 | 97.6s | 91.0% | 92.3% | 1 | 23/3 | 2026-03-22 23:04:21 |
| convert_number_to_words.py | github | gpt-4o-mini | 22 | 32.7s | 91.0% | 92.3% | 1 | 20/2 | 2026-03-22 23:04:53 |
| index.js | deepseek-chat | deepseek-chat | 108 | 401.3s | 26.9% | 19.8% | 3 | 0/108 | 2026-03-23 00:14:59 |
| index.js | deepseek-chat | deepseek-chat | 82 | 608.8s | 0.0% | 0.0% | 3 | 0/0 | 2026-03-23 11:56:33 |
| index.js | deepseek-chat | deepseek-chat | 96 | 580.8s | 69.3% | 62.6% | 3 | 33/0 | 2026-03-23 12:19:17 |
| index.js | deepseek-chat | deepseek-chat | 32 | 334.5s | 76.0% | 63.2% | 3 | 31/1 | 2026-03-23 12:40:56 |
| index.js | deepseek-chat | deepseek-chat | 38 | 365.5s | 72.7% | 63.7% | 3 | 37/1 | 2026-03-23 12:49:17 |
| index.js | deepseek-chat | deepseek-chat | 22 | 398.8s | 64.7% | 57.1% | 3 | 19/3 | 2026-03-23 13:06:18 |
| index.js | deepseek-chat | deepseek-chat | 36 | 262.4s | 76.5% | 63.7% | 3 | 33/58 | 2026-03-23 13:26:08 |
| index.js | deepseek-chat | deepseek-chat | 39 | 284.2s | 67.2% | 59.3% | 3 | 39/36 | 2026-03-23 13:52:59 |
| index.js | deepseek-reasoner | deepseek-reasoner | 27 | 498.0s | 97.1% | 85.2% | 2 | 28/17 | 2026-03-23 14:01:17 |
| index.js | github | gpt-4o-mini | 13 | 58.0s | 34.0% | 20.9% | 3 | 4/37 | 2026-03-23 14:06:03 |
| convert_number_to_words.py | deepseek-chat | deepseek-chat | 24 | 138.0s | 91.0% | 92.3% | 1 | 23/1 | 2026-03-23 15:42:15 |
| convert_number_to_words.py | deepseek-reasoner | deepseek-reasoner | 27 | 434.8s | 91.0% | 92.3% | 1 | 25/2 | 2026-03-23 15:49:30 |
| convert_number_to_words.py | google | gemini-2.5-flash | 28 | 97.5s | 91.0% | 92.3% | 1 | 25/3 | 2026-03-23 15:51:08 |
| convert_number_to_words.py | github | gpt-4o-mini | 15 | 38.8s | 85.9% | 84.6% | 3 | 11/4 | 2026-03-23 15:51:47 |
