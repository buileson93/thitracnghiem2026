import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for viewAdmin section
old_admin = '''        <!-- MÀN HÌNH 5: TRANG QUẢN TRỊ VIÊN (ADMIN PORTAL) -->
        <section id="viewAdmin" class="hidden max-w-5xl mx-auto space-y-6">
            <div class="bg-white rounded-2xl shadow-xl border border-slate-200 p-6">
                <div class="flex justify-between items-center pb-4 border-b border-slate-200 mb-6">
                    <div>
                        <h2 class="text-2xl font-bold text-slate-800 flex items-center">
                            <i class="fas fa-user-shield text-indigo-600 mr-3"></i> Quản Lý Hệ Thống Admin
                        </h2>
                        <p class="text-xs text-slate-500 mt-1">Cấu hình Cuộc thi, Nhập Excel/Google Sheets & Đơn vị</p>
                    </div>
                    <div class="flex items-center space-x-2">
                        <button onclick="logoutAdmin()" class="bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 px-3 py-1.5 rounded-lg text-xs font-semibold transition">
                            <i class="fas fa-sign-out-alt mr-1"></i> Đăng Xuất Admin
                        </button>
                </div>

                <!-- Admin Quick Action Toolbar -->
                <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6 bg-indigo-50/70 p-3.5 rounded-2xl border border-indigo-100 shadow-sm">
                    <button onclick="switchAdminTab('quizzes'); document.getElementById('addQuizTitle').focus();" class="flex items-center justify-center space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2.5 px-3 rounded-xl text-xs shadow-sm transition transform active:scale-95">
                        <i class="fas fa-plus-circle text-sm"></i>
                        <span>➕ Tạo Cuộc Thi Mới</span>
                    </button>
                    <button onclick="openAddQuestionManualModal()" class="flex items-center justify-center space-x-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2.5 px-3 rounded-xl text-xs shadow-sm transition transform active:scale-95">
                        <i class="fas fa-file-signature text-sm"></i>
                        <span>📝 Tạo 1 Câu Hỏi Mới</span>
                    </button>
                    <button onclick="switchAdminTab('questions'); document.getElementById('excelFileInput').click();" class="flex items-center justify-center space-x-2 bg-amber-500 hover:bg-amber-600 text-white font-bold py-2.5 px-3 rounded-xl text-xs shadow-sm transition transform active:scale-95">
                        <i class="fas fa-file-excel text-sm"></i>
                        <span>📄 Nạp Từ File Excel</span>
                    </button>
                    <button onclick="toggleBatchModal(true)" class="flex items-center justify-center space-x-2 bg-slate-800 hover:bg-slate-900 text-white font-bold py-2.5 px-3 rounded-xl text-xs shadow-sm transition transform active:scale-95">
                        <i class="fas fa-paste text-sm"></i>
                        <span>📋 Dán Văn Bản Batch</span>
                    </button>
                </div>

                <!-- Admin Tabs -->
                <div class="flex space-x-2 border-b border-slate-200 mb-6 overflow-x-auto">
                    <button id="adminTabQuizzesBtn" onclick="switchAdminTab('quizzes')" class="px-4 py-2 border-b-2 border-indigo-600 font-bold text-sm text-indigo-600 whitespace-nowrap">
                        <i class="fas fa-bullhorn mr-1"></i> Quản Lý Cuộc Thi (<span id="countQuizzesBadge">0</span>)
                    </button>
                    <button id="adminTabQuestionsBtn" onclick="switchAdminTab('questions')" class="px-4 py-2 border-b-2 border-transparent font-medium text-sm text-slate-500 hover:text-slate-800 whitespace-nowrap">
                        <i class="fas fa-file-excel mr-1"></i> Ngân Hàng Câu Hỏi & Excel (<span id="countQuestionsBadge">0</span>)
                    </button>
                    <button id="adminTabUnitsBtn" onclick="switchAdminTab('units')" class="px-4 py-2 border-b-2 border-transparent font-medium text-sm text-slate-500 hover:text-slate-800 whitespace-nowrap">
                        <i class="fas fa-sitemap mr-1"></i> Danh Sách Đơn Vị (<span id="countUnitsBadge">0</span>)
                    </button>
                </div>'''

new_admin = '''        <!-- MÀN HÌNH 5: TRANG QUẢN TRỊ VIÊN (EXECUTIVE ADMIN DASHBOARD) -->
        <section id="viewAdmin" class="hidden max-w-5xl mx-auto space-y-6">
            
            <!-- Admin Banner Header Card -->
            <div class="bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 rounded-3xl p-6 lg:p-8 text-white shadow-2xl border border-slate-800 flex flex-col md:flex-row justify-between items-start md:items-center gap-6 relative overflow-hidden">
                <div class="flex items-center space-x-4 relative z-10">
                    <div class="w-14 h-14 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 flex items-center justify-center text-amber-400 text-2xl shadow-inner shrink-0">
                        <i class="fas fa-user-shield"></i>
                    </div>
                    <div>
                        <div class="flex items-center space-x-2 mb-1">
                            <span class="bg-emerald-500/20 text-emerald-300 text-[10px] font-bold px-2.5 py-0.5 rounded-full border border-emerald-400/30 flex items-center">
                                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span>
                                ADMIN PORTAL ACTIVE
                            </span>
                        </div>
                        <h2 class="text-2xl font-extrabold font-heading text-white">Trung Tâm Quản Trị Hệ Thống</h2>
                        <p class="text-indigo-200 text-xs mt-0.5">Quản lý cuộc thi, ngân hàng câu hỏi, nạp Excel và cấu hình đơn vị</p>
                    </div>
                </div>

                <div class="flex items-center space-x-3 relative z-10 w-full md:w-auto justify-end">
                    <button onclick="logoutAdmin()" class="bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 border border-rose-400/40 px-4 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5">
                        <i class="fas fa-sign-out-alt"></i>
                        <span>Đăng Xuất Admin</span>
                    </button>
                    <button onclick="switchView('login')" class="bg-white/10 hover:bg-white/20 text-white border border-white/20 px-4 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5">
                        <i class="fas fa-home"></i>
                        <span>Trang Chủ</span>
                    </button>
                </div>
            </div>

            <!-- Executive Stat Overview Grid (4 Cards) -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-white p-4 rounded-2xl border border-slate-200/90 shadow-sm flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold text-lg shrink-0"><i class="fas fa-bullhorn"></i></div>
                    <div>
                        <span class="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Cuộc Thi</span>
                        <span id="countQuizzesBadge" class="text-xl font-extrabold text-slate-900">0</span>
                    </div>
                </div>
                <div class="bg-white p-4 rounded-2xl border border-slate-200/90 shadow-sm flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-lg shrink-0"><i class="fas fa-file-excel"></i></div>
                    <div>
                        <span class="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Ngân Hàng Đề</span>
                        <span id="countQuestionsBadge" class="text-xl font-extrabold text-slate-900">0</span>
                    </div>
                </div>
                <div class="bg-white p-4 rounded-2xl border border-slate-200/90 shadow-sm flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center font-bold text-lg shrink-0"><i class="fas fa-trophy"></i></div>
                    <div>
                        <span class="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Bảng Xếp Hạng</span>
                        <span class="text-xl font-extrabold text-slate-900">Active</span>
                    </div>
                </div>
                <div class="bg-white p-4 rounded-2xl border border-slate-200/90 shadow-sm flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-violet-100 text-violet-700 flex items-center justify-center font-bold text-lg shrink-0"><i class="fas fa-sitemap"></i></div>
                    <div>
                        <span class="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Đơn Vị</span>
                        <span id="countUnitsBadge" class="text-xl font-extrabold text-slate-900">0</span>
                    </div>
                </div>
            </div>

            <!-- Admin Main Workspace Container -->
            <div class="bg-white rounded-3xl shadow-xl border border-slate-200/90 p-6 lg:p-8 space-y-6">
                
                <!-- Quick Action Toolbar Card -->
                <div class="bg-slate-50 p-4 rounded-2xl border border-slate-200/80">
                    <span class="text-[11px] font-extrabold text-slate-500 uppercase tracking-wider block mb-3 font-heading">Thao Tác Nhanh Quản Trị</span>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                        <button onclick="switchAdminTab('quizzes'); document.getElementById('addQuizTitle').focus();" class="flex items-center justify-center space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2.5 px-3 rounded-xl text-xs shadow-sm transition transform active:scale-95">
                            <i class="fas fa-plus-circle text-sm"></i>
                            <span>➕ Tạo Cuộc Thi</span>
                        </button>
                        <button onclick="openAddQuestionManualModal()" class="flex items-center justify-center space-x-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2.5 px-3 rounded-xl text-xs shadow-sm transition transform active:scale-95">
                            <i class="fas fa-file-signature text-sm"></i>
                            <span>📝 Tạo 1 Câu Hỏi</span>
                        </button>
                        <button onclick="switchAdminTab('questions'); document.getElementById('excelFileInput').click();" class="flex items-center justify-center space-x-2 bg-amber-500 hover:bg-amber-600 text-white font-bold py-2.5 px-3 rounded-xl text-xs shadow-sm transition transform active:scale-95">
                            <i class="fas fa-file-excel text-sm"></i>
                            <span>📄 Nạp File Excel</span>
                        </button>
                        <button onclick="toggleBatchModal(true)" class="flex items-center justify-center space-x-2 bg-slate-800 hover:bg-slate-900 text-white font-bold py-2.5 px-3 rounded-xl text-xs shadow-sm transition transform active:scale-95">
                            <i class="fas fa-paste text-sm"></i>
                            <span>📋 Dán Batch Text</span>
                        </button>
                    </div>
                </div>

                <!-- Admin Tabs Bar -->
                <div class="flex space-x-2 border-b border-slate-200 pb-1 overflow-x-auto">
                    <button id="adminTabQuizzesBtn" onclick="switchAdminTab('quizzes')" class="px-5 py-3 rounded-xl font-bold text-xs text-indigo-700 bg-indigo-50 border border-indigo-200 whitespace-nowrap transition">
                        <i class="fas fa-bullhorn mr-1.5 text-sm"></i> Quản Lý Cuộc Thi
                    </button>
                    <button id="adminTabQuestionsBtn" onclick="switchAdminTab('questions')" class="px-5 py-3 rounded-xl font-medium text-xs text-slate-600 hover:bg-slate-50 border border-transparent whitespace-nowrap transition">
                        <i class="fas fa-file-excel mr-1.5 text-sm"></i> Ngân Hàng Câu Hỏi & Excel
                    </button>
                    <button id="adminTabUnitsBtn" onclick="switchAdminTab('units')" class="px-5 py-3 rounded-xl font-medium text-xs text-slate-600 hover:bg-slate-50 border border-transparent whitespace-nowrap transition">
                        <i class="fas fa-sitemap mr-1.5 text-sm"></i> Danh Sách Đơn Vị
                    </button>
                </div>'''

if old_admin in content:
    content = content.replace(old_admin, new_admin)
    print("Redesigned viewAdmin executive dashboard successfully")
else:
    print("Could not find old_admin in index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
