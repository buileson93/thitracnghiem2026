import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Network Time Offset and Security State Variables
old_vars = '''        let activeQuizzesList = [DEFAULT_QUIZ];
        let activeQuestionsPool = EMBEDDED_QUESTIONS;
        let activeUnitsList = [];
        let currentQuizQuestions = [];
        let userAnswers = {};
        let timerInterval = null;
        let timeElapsedSeconds = 0;
        let rawSubmissions = [];
        let pendingExcelQuestions = []; // Danh sách câu hỏi chờ xác nhận lưu'''

new_vars = '''        let activeQuizzesList = [DEFAULT_QUIZ];
        let activeQuestionsPool = EMBEDDED_QUESTIONS;
        let activeUnitsList = [];
        let currentQuizQuestions = [];
        let userAnswers = {};
        let timerInterval = null;
        let timeElapsedSeconds = 0;
        let rawSubmissions = [];
        let pendingExcelQuestions = []; // Danh sách câu hỏi chờ xác nhận lưu

        // CHỐNG GIAN LẬN & ĐỒNG BỘ THỜI GIAN MẠNG
        let networkTimeOffset = 0; // Độ lệch giữa giờ máy chủ mạng và giờ máy tính local
        let isExamSecurityActive = false; // Trạng thái bảo vệ phòng thi
        let examTabSwitchCount = 0; // Số lần vi phạm chuyển tab'''

if old_vars in content:
    content = content.replace(old_vars, new_vars)
    print("Injected security state variables successfully")
else:
    print("Could not find old_vars in index.html")

# 2. Add Network Time Sync & Security Protection Functions
security_js = '''
        // =========================================================================
        // 🌐 HỆ THỐNG CHỐNG GIAN LẬN & ĐỒNG BỘ THỜI GIAN MẠNG REALTIME
        // =========================================================================
        async function syncNetworkTime() {
            window.syncNetworkTime = syncNetworkTime;
            try {
                const startLocal = Date.now();
                // Lấy giờ chuẩn mạng quốc tế (World Time API hoặc TimeAPI)
                const res = await fetch('https://worldtimeapi.org/api/timezone/Asia/Ho_Chi_Minh', { cache: 'no-store' });
                if (res.ok) {
                    const data = await res.json();
                    const serverTime = new Date(data.datetime).getTime();
                    const roundtrip = (Date.now() - startLocal) / 2;
                    networkTimeOffset = (serverTime + roundtrip) - Date.now();
                    console.log("🌐 Đồng bộ giờ mạng thành công. Độ lệch:", networkTimeOffset, "ms");
                    updateNetworkTimeBadge(true);
                }
            } catch (err) {
                console.warn("Lỗi đồng bộ WorldTime API, dùng thời gian hệ thống chuẩn:", err);
                updateNetworkTimeBadge(false);
            }
        }

        function getNetworkNow() {
            window.getNetworkNow = getNetworkNow;
            return new Date(Date.now() + networkTimeOffset);
        }

        function updateNetworkTimeBadge(isSynced) {
            const badge = document.getElementById('networkTimeBadge');
            if (badge) {
                if (isSynced) {
                    badge.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span> Giờ mạng chuẩn: <b class="ml-1">${getNetworkNow().toLocaleTimeString('vi-VN')}</b>`;
                    badge.className = "inline-flex items-center px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-600 border border-emerald-300/50";
                } else {
                    badge.innerHTML = `<span class="w-2 h-2 rounded-full bg-amber-400 mr-1.5"></span> Giờ hệ thống: <b class="ml-1">${getNetworkNow().toLocaleTimeString('vi-VN')}</b>`;
                }
            }
        }

        // BẬT BẢO VỆ CHỐNG GIAN LẬN PHÒNG THI
        function enableExamSecurity() {
            window.enableExamSecurity = enableExamSecurity;
            isExamSecurityActive = true;
            examTabSwitchCount = 0;

            // Khóa Chuột Phải, Bôi Đen & Phím Tắt Tra Cứu
            document.addEventListener('contextmenu', blockExamAction);
            document.addEventListener('copy', blockExamAction);
            document.addEventListener('cut', blockExamAction);
            document.addEventListener('selectstart', blockExamAction);
            document.addEventListener('keydown', blockKeyShortcuts);

            // Giám sát Chuyển Tab / Out khỏi Phòng Thi
            window.addEventListener('blur', handleExamTabLeave);
            document.addEventListener('visibilitychange', handleExamVisibilityChange);

            // Áp CSS Khóa Chọn Văn Bản
            document.getElementById('viewQuiz').style.userSelect = 'none';
            document.getElementById('viewQuiz').style.webkitUserSelect = 'none';
        }

        // TẮT BẢO VỆ PHÒNG THI
        function disableExamSecurity() {
            window.disableExamSecurity = disableExamSecurity;
            isExamSecurityActive = false;

            document.removeEventListener('contextmenu', blockExamAction);
            document.removeEventListener('copy', blockExamAction);
            document.removeEventListener('cut', blockExamAction);
            document.removeEventListener('selectstart', blockExamAction);
            document.removeEventListener('keydown', blockKeyShortcuts);

            window.removeEventListener('blur', handleExamTabLeave);
            document.removeEventListener('visibilitychange', handleExamVisibilityChange);

            if (document.getElementById('viewQuiz')) {
                document.getElementById('viewQuiz').style.userSelect = 'auto';
                document.getElementById('viewQuiz').style.webkitUserSelect = 'auto';
            }
        }

        function blockExamAction(e) {
            if (isExamSecurityActive) {
                e.preventDefault();
                showStatus("⚠️ HỆ THỐNG KHÓA THAO TÁC: Không được copy hoặc dùng chuột phải trong phòng thi!", "error");
                return false;
            }
        }

        function blockKeyShortcuts(e) {
            if (!isExamSecurityActive) return;

            // Khóa F12, Ctrl+Shift+I, Cmd+Opt+I (DevTools)
            // Khóa Ctrl+C, Cmd+C, Ctrl+U, Cmd+U, Ctrl+P, Cmd+P
            const isCmdOrCtrl = e.ctrlKey || e.metaKey;
            const key = e.key.toLowerCase();

            if (e.keyCode === 123 || (isCmdOrCtrl && (key === 'c' || key === 'u' || key === 'p' || key === 'a' || key === 's' || key === 'i'))) {
                e.preventDefault();
                showStatus("⚠️ HỆ THỐNG KHÓA PHÍM TẮT: Thao tác bị cấm trong giờ thi!", "error");
                return false;
            }
        }

        function handleExamTabLeave() {
            if (isExamSecurityActive) {
                disqualifyExam("Phát hiện chuyển cửa sổ / rời màn hình thi!");
            }
        }

        function handleExamVisibilityChange() {
            if (isExamSecurityActive && document.hidden) {
                disqualifyExam("Phát hiện chuyển tab trình duyệt ra ngoài!");
            }
        }

        // HỦY BÀI THI & YÊU CẦU THI LẠI TỪ ĐẦU KHI VI PHẠM
        function disqualifyExam(reason) {
            window.disqualifyExam = disqualifyExam;
            if (!isExamSecurityActive) return;

            disableExamSecurity();
            if (timerInterval) clearInterval(timerInterval);

            alert(`⚠️ CẢNH BÁO VI PHẠM QUY ĐỊNH THI!\\n\\nLý do: ${reason}\\n\\nBài thi của bạn đã bị HỦY BỎ. Bạn bắt buộc phải thi lại từ đầu!`);
            
            userAnswers = {};
            currentQuizQuestions = [];
            timeElapsedSeconds = 0;
            switchView('login');
            showStatus("Bài thi đã bị hủy do vi phạm quy định chống gian lận!", "error");
        }
'''

content = content.replace("        let activeQuizzesList = [DEFAULT_QUIZ];", security_js + "\n        let activeQuizzesList = [DEFAULT_QUIZ];")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected Network Time & Anti-Cheating System successfully")
