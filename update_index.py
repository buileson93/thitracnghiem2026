import json

with open('questions_data.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Assign default quizId to all 105 questions
for q in questions:
    q['quizId'] = 'j814OsorghaODen4HRZr'

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace activeQuizzesList and activeQuestionsPool initial state
js_embedded = '''
        const DEFAULT_QUIZ = {
            firestoreId: "j814OsorghaODen4HRZr",
            title: "Cuộc Thi Tiết Kiệm 2026 (Nghị định 265/2026/NĐ-CP)",
            description: "Bộ 105 câu hỏi đánh giá kiến thức về Tiết kiệm, chống lãng phí",
            startTime: "2026-01-01T00:00",
            endTime: "2030-12-31T23:59",
            isActive: true
        };

        const EMBEDDED_QUESTIONS = ''' + json.dumps(questions, ensure_ascii=False, indent=2) + ''';

        let activeQuizzesList = [DEFAULT_QUIZ];
        let activeQuestionsPool = EMBEDDED_QUESTIONS;'''

old_vars = '''        let activeQuizzesList = [];
        let activeQuestionsPool = [];'''

if old_vars in html:
    html = html.replace(old_vars, js_embedded)
    print('Replaced activeQuizzesList and activeQuestionsPool successfully')
else:
    print('Could not find old_vars in html')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
