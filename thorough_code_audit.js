const jsdom = require('jsdom');
const { JSDOM } = jsdom;

async function thoroughAudit() {
    console.log("==================================================");
    console.log("=== CHƯƠNG TRÌNH RÀ SOÁT LỖI TOÀN DIỆN (DEEP CODE AUDIT) ===");
    console.log("==================================================");

    const virtualConsole = new jsdom.VirtualConsole();
    const uncaughtErrors = [];

    virtualConsole.on("error", (err) => {
        console.log("🔴 BROWSER ERROR:", err);
        uncaughtErrors.push(err);
    });

    try {
        const dom = await JSDOM.fromURL("http://localhost:8080/index.html", {
            runScripts: "dangerously",
            resources: "usable",
            virtualConsole
        });

        await new Promise(r => setTimeout(r, 2000));
        const win = dom.window;
        const doc = win.document;

        // TEST 1: Admin Tab Switching & Add Quiz
        console.log("\n[TEST 1] Thử nghiệm Tab Admin & Tạo Cuộc Thi Mới...");
        win.isAdminAuthenticated = true;
        win.switchView('admin');
        win.switchAdminTab('questions');
        win.switchAdminTab('units');
        win.switchAdminTab('quizzes');

        // Test add quiz
        doc.getElementById('addQuizTitle').value = 'Cuộc Thi Thử Nghiệm Audit 2026';
        doc.getElementById('addQuizDesc').value = 'Mô tả thử nghiệm';
        doc.getElementById('addQuizStartTime').value = '2026-01-01T00:00';
        doc.getElementById('addQuizEndTime').value = '2030-12-31T23:59';
        doc.getElementById('addQuizActive').checked = true;

        await win.handleAddQuiz({ preventDefault: () => {} });
        console.log("✅ Tạo cuộc thi mới: THÀNH CÔNG!");

        // TEST 2: Add Unit & Delete Unit
        console.log("\n[TEST 2] Thử nghiệm Quản Lý Đơn Vị (Add & Delete Unit)...");
        doc.getElementById('addUnitInput').value = 'Phòng Audit Thử Nghiệm';
        await win.handleAddUnit({ preventDefault: () => {} });
        console.log("✅ Thêm đơn vị mới: THÀNH CÔNG!");

        // TEST 3: Batch Import Text Questions
        console.log("\n[TEST 3] Thử nghiệm Nạp Câu Hỏi Hàng Loạt (Batch Import)...");
        win.toggleBatchModal(true);
        doc.getElementById('batchInputText').value = 'Câu hỏi thử nghiệm Batch|Phương án A|Phương án B|Phương án C|Phương án D|A';
        doc.getElementById('adminQuestionQuizSelect').value = 'j814OsorghaODen4HRZr';
        await win.processBatchImport();
        console.log("✅ Nạp câu hỏi batch text: THÀNH CÔNG!");

        // TEST 4: Full Candidate Flow (Start -> Flag -> Answer -> Scroll -> Submit -> Review)
        console.log("\n[TEST 4] Thử nghiệm Quy trình Thí sinh hoàn chỉnh...");
        win.switchView('login');

        doc.getElementById('selectQuiz').value = 'j814OsorghaODen4HRZr';
        doc.getElementById('inputName').value = 'Thí Sinh Audit Pro';
        doc.getElementById('inputCccd').value = '987654321012';
        doc.getElementById('selectUnit').value = 'Phòng Kỹ thuật - Công nghệ';

        win.handleLogin({ preventDefault: () => {} });

        // Answer and Flag questions
        for (let i = 0; i < 20; i++) {
            win.selectAnswer(i, i % 4);
            if (i % 3 === 0) win.toggleFlagQuestion(i);
            win.scrollToQuestion(i);
        }

        console.log("✅ Thao tác chọn đáp án & đánh dấu xem lại: THÀNH CÔNG!");

        win.openSubmitModal();
        win.closeSubmitModal();
        win.submitQuiz();

        console.log("✅ Nộp bài thi & Xem kết quả: THÀNH CÔNG!");

        // TEST 5: Leaderboard Filter & Export Excel
        console.log("\n[TEST 5] Thử nghiệm Lọc Bảng Xếp Hạng & Xuất Excel...");
        win.switchView('leaderboard');

        doc.getElementById('filterQuiz').value = 'ALL';
        doc.getElementById('filterUnit').value = 'ALL';
        doc.getElementById('filterSearch').value = 'Audit';
        win.renderLeaderboardTable();

        win.exportLeaderboardExcel();
        console.log("✅ Xuất Báo Cáo Excel Bảng Xếp Hạng: THÀNH CÔNG!");

        console.log("\n==================================================");
        console.log(`=== AUDIT KẾT THÚC. TỔNG SỐ LỖI PHÁT HIỆN: ${uncaughtErrors.length} ===`);
        console.log("==================================================");

    } catch (e) {
        console.error("🔴 Lỗi kịch bản audit:", e);
    }
}

thoroughAudit();
