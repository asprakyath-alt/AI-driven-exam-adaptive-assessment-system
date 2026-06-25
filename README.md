EAMCET & JEE Mains Preparation Platform

📁 Project Structure
```
eamcet_app/
├── app.py                       
└── data/
    ├── students.csv        
    ├── questions.csv        
    ├── results.csv       
    ├── mistakes.csv         
    ├── challenges.csv       
    └── challenge_results.csv


# Features

| Features |
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

# 🗃️ Scoring System

- ✅ Correct answer → *+4 marks*
- ❌ Wrong answer (neg marking on) → *−1 mark*
- ⏭️ Unattempted → *0 marks*

# Enable Full AI Tutor

In `app.py`, find the AI Tutor section and replace the keyword response with:

# 📝 Adding Questions

Either:
* Use **Admin Panel → Add Question** in the app


All data is stored in CSV files in the `data/` folder.

