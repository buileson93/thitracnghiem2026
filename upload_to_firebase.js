const fs = require('fs');

const API_KEY = "AIzaSyDEo3uJzrC7AtQXhQ2K5XISPln7upLjZNQ";
const PROJECT_ID = "mirats101";
const APP_ID = "default-quiz-app";
const BASE_URL = `https://firestore.googleapis.com/v1/projects/${PROJECT_ID}/databases/(default)/documents`;

async function main() {
    console.log("1. Đang đăng nhập ẩn danh vào Firebase...");
    const authRes = await fetch(`https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=${API_KEY}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ returnSecureToken: true })
    });
    const authData = await authRes.json();
    if (!authData.idToken) {
        console.error("Lỗi đăng nhập Firebase:", authData);
        process.exit(1);
    }
    const token = authData.idToken;
    console.log("-> Đăng nhập Firebase thành công!");

    // 2. Tạo cuộc thi mới trên Firestore
    console.log("\n2. Đang tạo Cuộc thi 'Cuộc thi Tiết kiệm 2026' trên Firebase Firestore...");
    const quizTitle = "Cuộc Thi Tiết Kiệm 2026 (Nghị định 265/2026/NĐ-CP)";
    const quizDesc = "Bộ câu hỏi đánh giá kiến thức về Tiết kiệm, chống lãng phí theo Nghị định 265/2026/NĐ-CP (105 câu hỏi).";
    
    const now = new Date();
    const endDate = new Date();
    endDate.setDate(now.getDate() + 90);

    const quizDocData = {
        fields: {
            title: { stringValue: quizTitle },
            description: { stringValue: quizDesc },
            startTime: { stringValue: now.toISOString().slice(0, 16) },
            endTime: { stringValue: endDate.toISOString().slice(0, 16) },
            isActive: { booleanValue: true },
            createdAt: { timestampValue: now.toISOString() }
        }
    };

    const quizRes = await fetch(`${BASE_URL}/artifacts/${APP_ID}/public/data/quizzes`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(quizDocData)
    });

    const quizCreated = await quizRes.json();
    if (!quizCreated.name) {
        console.error("Lỗi tạo cuộc thi:", quizCreated);
        process.exit(1);
    }

    // Extract doc ID
    const quizId = quizCreated.name.split('/').pop();
    console.log(`-> Đã tạo thành công cuộc thi với ID: ${quizId}`);

    // 3. Upload 105 câu hỏi
    console.log("\n3. Đang tải 105 câu hỏi lên Firebase Firestore...");
    const questions = JSON.parse(fs.readFileSync('questions_data.json', 'utf-8'));

    let count = 0;
    for (const q of questions) {
        const qDocData = {
            fields: {
                quizId: { stringValue: quizId },
                question: { stringValue: q.question },
                options: {
                    arrayValue: {
                        values: q.options.map(opt => ({ stringValue: opt }))
                    }
                },
                correctIndex: { integerValue: q.correctIndex },
                createdAt: { timestampValue: new Date().toISOString() }
            }
        };

        const qRes = await fetch(`${BASE_URL}/artifacts/${APP_ID}/public/data/questions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(qDocData)
        });

        if (qRes.ok) {
            count++;
            process.stdout.write(`\rĐã tải: ${count}/${questions.length} câu hỏi`);
        } else {
            console.error(`\nLỗi tải câu hỏi "${q.question}":`, await qRes.json());
        }
    }

    console.log(`\n\n🎉 HOÀN THÀNH! Đã upload thành công cuộc thi "${quizTitle}" (ID: ${quizId}) và ${count} câu hỏi lên Firebase Firestore!`);
}

main().catch(err => console.error(err));
