import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Enhance Google Fonts in <head>
old_head = '''    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
    </style>'''

new_head = '''    <!-- Google Fonts: Inter & Outfit -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        h1, h2, h3, h4, .font-heading { font-family: 'Outfit', 'Inter', sans-serif; }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(226, 232, 240, 0.8);
        }
        
        .glass-header {
            background: rgba(79, 70, 229, 0.95);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }
        
        .pulse-timer {
            animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        
        @keyframes pulse-ring {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.85; transform: scale(1.02); }
        }

        .option-card {
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .option-card:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px -2px rgba(79, 70, 229, 0.12);
        }
    </style>'''

if old_head in content:
    content = content.replace(old_head, new_head)
    print("Enhanced Google Fonts & CSS design system")

# 2. Add Export Leaderboard to Excel function to JavaScript
export_excel_func = '''
        function exportLeaderboardExcel() {
            window.exportLeaderboardExcel = exportLeaderboardExcel;
            if (!rawSubmissions || rawSubmissions.length === 0) {
                showStatus("Chưa có dữ liệu kết quả thi để xuất Excel!", "error");
                return;
            }

            let sorted = [...rawSubmissions].sort((a, b) => {
                if (b.score !== a.score) return b.score - a.score;
                return a.timeSeconds - b.timeSeconds;
            });

            const data = [
                ["STT", "Họ và Tên", "Số CCCD", "Đơn Vị / Phòng Ban", "Cuộc Thi", "Số Câu Đúng", "Tổng Số Câu", "Thời Gian Làm Bài", "Ngày Thi"]
            ];

            sorted.forEach((item, idx) => {
                data.push([
                    idx + 1,
                    item.name || '',
                    item.cccd || '',
                    item.unit || '',
                    item.quizTitle || '',
                    item.score || 0,
                    20,
                    item.timeFormatted || '00:00',
                    item.dateStr || ''
                ]);
            });

            const ws = XLSX.utils.aoa_to_sheet(data);
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, "KetQuaThi");
            XLSX.writeFile(wb, `BaoCao_KetQuaThi_${new Date().toISOString().slice(0,10)}.xlsx`);
            showStatus("Đã xuất báo cáo kết quả thi ra file Excel thành công!", "success");
        }
'''

# Add flag question functionality
flag_func = '''
        let flaggedQuestions = {};

        function toggleFlagQuestion(qIdx) {
            window.toggleFlagQuestion = toggleFlagQuestion;
            flaggedQuestions[qIdx] = !flaggedQuestions[qIdx];
            const flagBtn = document.getElementById(`flag-btn-${qIdx}`);
            const gridBtn = document.getElementById(`grid-btn-${qIdx}`);
            
            if (flagBtn) {
                if (flaggedQuestions[qIdx]) {
                    flagBtn.className = "px-3 py-1.5 rounded-lg text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-300 transition flex items-center space-x-1";
                    flagBtn.innerHTML = `<i class="fas fa-flag text-amber-600"></i> <span>Đã Đánh Dấu</span>`;
                } else {
                    flagBtn.className = "px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 text-slate-600 border border-slate-200 hover:bg-slate-200 transition flex items-center space-x-1";
                    flagBtn.innerHTML = `<i class="far fa-flag mr-1"></i> <span>Đánh Dấu Xem Lại</span>`;
                }
            }

            if (gridBtn) {
                if (flaggedQuestions[qIdx]) {
                    gridBtn.classList.add('ring-2', 'ring-amber-400');
                } else {
                    gridBtn.classList.remove('ring-2', 'ring-amber-400');
                }
            }
        }
'''

# Insert functions before </script>
content = content.replace("        function showStatus(msg, type) {", export_excel_func + "\n" + flag_func + "\n        function showStatus(msg, type) {")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully injected exportLeaderboardExcel and toggleFlagQuestion functions")
