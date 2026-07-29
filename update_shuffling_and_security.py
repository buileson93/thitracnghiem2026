import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace prepareQuiz
old_prepare = '''        function prepareQuiz() {
            window.prepareQuiz = prepareQuiz;
            userAnswers = {};
            timeElapsedSeconds = 0;

            let quizQuestionsPool = activeQuestionsPool.filter(q => q.quizId === userData.quizId);
            if (quizQuestionsPool.length < 20 && activeQuestionsPool.length >= 20) {
                quizQuestionsPool = activeQuestionsPool;
            }
            const shuffled = [...quizQuestionsPool].sort(() => 0.5 - Math.random());
            currentQuizQuestions = shuffled.slice(0, 20);

            document.getElementById('quizTitleDisplay').textContent = userData.quizTitle;
            document.getElementById('userInfoDisplay').textContent = `${userData.name} (${userData.cccd})`;
            document.getElementById('userUnitDisplay').textContent = userData.unit;

            renderQuizQuestions();
            renderQuestionGrid();
            startTimer();

            switchView('quiz');
        }'''

new_prepare = '''        function prepareQuiz() {
            window.prepareQuiz = prepareQuiz;
            userAnswers = {};
            timeElapsedSeconds = 0;

            let quizQuestionsPool = activeQuestionsPool.filter(q => q.quizId === userData.quizId);
            if (quizQuestionsPool.length < 20 && activeQuestionsPool.length >= 20) {
                quizQuestionsPool = activeQuestionsPool;
            }
            
            // 1. TRÁO NGẪU NHIÊN DANH SÁCH 20 CÂU HỎI
            const shuffledQuestions = [...quizQuestionsPool].sort(() => 0.5 - Math.random());
            
            // 2. TRÁO NGẪU NHIÊN CÁC ĐÁP ÁN (A, B, C, D) CỦA TỪNG CÂU & ĐỒNG BỘ ÁP MÃ CHẤM ĐIỂM CHUẨN
            currentQuizQuestions = shuffledQuestions.slice(0, 20).map(q => {
                const originalOptions = [...q.options];
                const originalCorrectText = originalOptions[q.correctIndex];
                
                // Shuffle options A, B, C, D
                const shuffledOptions = [...originalOptions].sort(() => 0.5 - Math.random());
                const newCorrectIndex = shuffledOptions.indexOf(originalCorrectText);
                
                return {
                    ...q,
                    options: shuffledOptions,
                    correctIndex: newCorrectIndex,
                    originalCorrectText: originalCorrectText
                };
            });

            document.getElementById('quizTitleDisplay').textContent = userData.quizTitle;
            document.getElementById('userInfoDisplay').textContent = `${userData.name} (${userData.cccd})`;
            document.getElementById('userUnitDisplay').textContent = userData.unit;

            renderQuizQuestions();
            renderQuestionGrid();
            startTimer();

            // 3. KÍCH HOẠT HỆ THỐNG BẢO VỆ CHỐNG GIAN LẬN & ĐỒNG BỘ GIỜ MẠNG
            enableExamSecurity();
            syncNetworkTime();

            switchView('quiz');
        }'''

if old_prepare in content:
    content = content.replace(old_prepare, new_prepare)
    print("Replaced prepareQuiz successfully")

# Replace submitQuiz
old_submit = '''        async function submitQuiz() {
            window.submitQuiz = submitQuiz;
            closeSubmitModal();
            clearInterval(timerInterval);'''

new_submit = '''        async function submitQuiz() {
            window.submitQuiz = submitQuiz;
            closeSubmitModal();
            clearInterval(timerInterval);
            disableExamSecurity(); // Tắt bảo vệ phòng thi sau khi đã nộp bài'''

if old_submit in content:
    content = content.replace(old_submit, new_submit)
    print("Replaced submitQuiz successfully")

# Also ensure syncNetworkTime is called on app init
if "listenToQuizzes();" in content:
    content = content.replace("listenToQuizzes();", "listenToQuizzes();\n                syncNetworkTime();")
    print("Added syncNetworkTime to app init")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
