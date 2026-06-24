# 🎓 EduPrepPro — EAMCET & JEE Mains Preparation Platform

## 🚀 Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🔑 Demo Login Credentials

| Role    | Username       | Password  |
|---------|---------------|-----------|
| Admin   | `admin`        | `admin123`|
| Student | `ravi_kumar`   | `pass123` |
| Student | `priya_sharma` | `pass123` |
| Student | `arjun_reddy`  | `pass123` |
| Student | `sneha_patel`  | `pass123` |
| Student | `kiran_babu`   | `pass123` |

## 📁 Project Structure

```
eamcet_app/
├── app.py                    ← Main Streamlit application (~700 lines)
├── requirements.txt          ← Python dependencies
├── README.md
└── data/
    ├── students.csv          ← User accounts (username/password/role)
    ├── questions.csv         ← 45 questions (Physics/Chemistry/Maths)
    ├── results.csv           ← Test history
    ├── mistakes.csv          ← Wrong answers notebook
    ├── challenges.csv        ← Live challenge definitions
    └── challenge_results.csv ← Challenge leaderboard data
```

## ✨ All Pages & Features

| Page | Features |
|------|----------|
| 🏠 Home | Animated hero, feature grid, exam info, quick stats |
| 📊 Dashboard | 5 KPI cards, trend chart, bar chart, donut chart, strength analysis |
| 📚 Materials | Theory notes, Practice Q&A, AI Tutor chatbot |
| ✏️ Daily Practice | 10 random questions, scored review, auto-save mistakes |
| 📝 Take Test | Subject/chapter/timer/neg-marking config, live timer, auto-submit, solutions |
| ⚔️ Challenges | Active/upcoming/completed challenges, per-challenge leaderboard |
| 🏆 Leaderboard | Global rankings, bar chart |
| 📖 Mistake Notebook | Review wrong answers, bookmark, delete, filter |
| ⚙️ Admin Panel | Overview charts, add/delete questions, student reports, challenge management |

## 🗃️ Scoring System

- ✅ Correct answer → **+4 marks**
- ❌ Wrong answer (neg marking on) → **−1 mark**
- ⏭️ Unattempted → **0 marks**

## 🔧 Enable Full AI Tutor

In `app.py`, find the AI Tutor section and replace the keyword response with:

```python
import anthropic
client = anthropic.Anthropic(api_key="YOUR_KEY_HERE")
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": user_q}]
)
answer = response.content[0].text
```

## 📝 Adding Questions

Either:
1. Use **Admin Panel → Add Question** in the app
2. Or run the app and use admin login to manage questions

All data is stored in CSV files in the `data/` folder.

## 🐛 Bugs Fixed in This Version

- CSV parsing error (commas inside question fields)
- `KeyError: test_config` on page load
- Unsafe `groupby` lambda referencing outer DataFrame
- `bookmarked` boolean string comparison (`"True"` vs `True`)
- `question_id` type mismatch (int vs int64)
- `challenge_id` type mismatch in leaderboard filter
- `value_counts()` column naming (pandas version compatibility)
- `format_func` lambda variable capture corrected
- `st.rerun()` placement fixed (outside forms)
- Navigation emoji stripping made robust
- All `st.session_state` keys initialised before access
- `avg_accuracy` NaN filled with 0 after merge
"# AI-driven-exam-adaptive-assessment-system" 
