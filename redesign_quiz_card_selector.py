import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Candidate Login form markup to replace selectQuiz with Quiz Selection Cards Grid
old_select_markup = '''                        <div>
                            <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1 flex items-center">
                                <i class="fas fa-bullhorn text-indigo-600 mr-1.5"></i> Cuộc Thi / Đợt Thi <span class="text-red-500 ml-1">*</span>
                            </label>
                            <select id="selectQuiz" onchange="onQuizSelectChange()" required class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-600 outline-none transition bg-slate-50 font-bold text-slate-800 text-xs md:text-sm">
                                <option value="j814OsorghaODen4HRZr">Cuộc Thi Tiết Kiệm 2026 (Nghị định 265/2026/NĐ-CP) [Đang diễn ra]</option>
                            </select>
                        </div>'''

new_select_markup = '''                        <div>
                            <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2 flex items-center justify-between">
                                <span><i class="fas fa-bullhorn text-indigo-600 mr-1.5"></i> Chọn Cuộc Thi Tham Gia <span class="text-red-500 ml-1">*</span></span>
                                <span class="text-[10px] text-slate-400 font-normal">Click chọn 1 cuộc thi bên dưới</span>
                            </label>
                            <!-- Hidden Select input for compatibility -->
                            <input type="hidden" id="selectQuiz" required value="j814OsorghaODen4HRZr">
                            
                            <!-- Interactive Card Selection Container -->
                            <div id="quizCardsContainer" class="space-y-3 max-h-60 overflow-y-auto pr-1"></div>
                        </div>'''

if old_select_markup in content:
    content = content.replace(old_select_markup, new_select_markup)
    print("Replaced selectQuiz markup with quizCardsContainer successfully")

# 2. Update updateQuizDropdowns JS function to render Quiz Cards
old_dropdown_js = '''            selectQuiz.innerHTML = `<option value="">-- Chọn cuộc thi tham gia --</option>` + quizOptions;
            filterQuiz.innerHTML = `<option value="ALL">-- Tất cả cuộc thi --</option>` + activeQuizzesList.map(q => `<option value="${q.firestoreId}">${q.title}</option>`).join('');
            
            if (adminQuestionQuizSelect) {
                const currentVal = adminQuestionQuizSelect.value;
                adminQuestionQuizSelect.innerHTML = activeQuizzesList.length > 0 
                    ? activeQuizzesList.map(q => `<option value="${q.firestoreId}">${q.title}</option>`).join('')
                    : `<option value="">-- Chưa có cuộc thi --</option>`;
                
                if (currentVal && activeQuizzesList.some(q => q.firestoreId === currentVal)) {
                    adminQuestionQuizSelect.value = currentVal;
                } else if (activeQuizzesList.length > 0) {
                    adminQuestionQuizSelect.value = activeQuizzesList[0].firestoreId;
                }
            }

            if (activeQuizzesList.length > 0 && !selectQuiz.value) {
                selectQuiz.value = activeQuizzesList[0].firestoreId;
                onQuizSelectChange();
            }'''

new_dropdown_js = '''            // Render Interactive Quiz Cards Container
            const cardsContainer = document.getElementById('quizCardsContainer');
            const hiddenSelect = document.getElementById('selectQuiz');

            if (cardsContainer) {
                if (activeQuizzesList.length === 0) {
                    cardsContainer.innerHTML = `<p class="text-xs text-slate-400 italic p-3 bg-slate-50 rounded-xl border">Hiện chưa có cuộc thi nào active.</p>`;
                } else {
                    const currentSelectedId = hiddenSelect.value || activeQuizzesList[0].firestoreId;
                    hiddenSelect.value = currentSelectedId;

                    cardsContainer.innerHTML = activeQuizzesList.map(q => {
                        const timeStatus = checkQuizTimeStatus(q);
                        const isSelected = q.firestoreId === currentSelectedId;
                        const statusBadgeClass = timeStatus.status === 'ONGOING'
                            ? 'bg-emerald-100 text-emerald-700 border-emerald-300'
                            : timeStatus.status === 'NOT_STARTED'
                            ? 'bg-amber-100 text-amber-700 border-amber-300'
                            : 'bg-slate-100 text-slate-600 border-slate-300';

                        return `
                            <div onclick="selectQuizCard('${q.firestoreId}')" id="quiz-card-${q.firestoreId}" class="quiz-card group p-3.5 rounded-2xl border-2 ${isSelected ? 'border-indigo-600 bg-indigo-50/60 ring-2 ring-indigo-500/20' : 'border-slate-200 bg-white hover:border-indigo-300 hover:bg-slate-50'} cursor-pointer transition-all shadow-sm">
                                <div class="flex justify-between items-start gap-2 mb-1.5">
                                    <div class="flex items-start space-x-2.5 flex-1 min-w-0">
                                        <div class="radio-check w-4 h-4 rounded-full border-2 ${isSelected ? 'border-indigo-600 bg-indigo-600' : 'border-slate-400 group-hover:border-indigo-600'} flex items-center justify-center shrink-0 mt-0.5 transition">
                                            <div class="w-1.5 h-1.5 rounded-full bg-white ${isSelected ? 'block' : 'hidden'}"></div>
                                        </div>
                                        <div class="min-w-0 flex-1">
                                            <h4 class="font-extrabold text-xs md:text-sm text-slate-800 leading-snug break-words group-hover:text-indigo-700 transition font-heading">${q.title}</h4>
                                            ${q.description ? `<p class="text-[11px] text-slate-500 mt-0.5 line-clamp-2 leading-normal">${q.description}</p>` : ''}
                                        </div>
                                    </div>
                                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold border shrink-0 ${statusBadgeClass}">
                                        ${timeStatus.text}
                                    </span>
                                </div>
                                <div class="flex items-center space-x-3 text-[10px] text-slate-500 font-medium pl-6 pt-1 border-t border-slate-100/80 mt-1.5">
                                    <span><i class="far fa-clock text-indigo-500 mr-1"></i>${formatDateTimeDisplay(q.startTime)} - ${formatDateTimeDisplay(q.endTime)}</span>
                                </div>
                            </div>
                        `;
                    }).join('');
                }
            }

            if (filterQuiz) {
                filterQuiz.innerHTML = `<option value="ALL">-- Tất cả cuộc thi --</option>` + activeQuizzesList.map(q => `<option value="${q.firestoreId}">${q.title}</option>`).join('');
            }
            
            if (adminQuestionQuizSelect) {
                const currentVal = adminQuestionQuizSelect.value;
                adminQuestionQuizSelect.innerHTML = activeQuizzesList.length > 0 
                    ? activeQuizzesList.map(q => `<option value="${q.firestoreId}">${q.title}</option>`).join('')
                    : `<option value="">-- Chưa có cuộc thi --</option>`;
                
                if (currentVal && activeQuizzesList.some(q => q.firestoreId === currentVal)) {
                    adminQuestionQuizSelect.value = currentVal;
                } else if (activeQuizzesList.length > 0) {
                    adminQuestionQuizSelect.value = activeQuizzesList[0].firestoreId;
                }
            }'''

if old_dropdown_js in content:
    content = content.replace(old_dropdown_js, new_dropdown_js)
    print("Replaced updateQuizDropdowns JS successfully")

# 3. Add selectQuizCard JS handler
select_card_js = '''
        function selectQuizCard(quizId) {
            window.selectQuizCard = selectQuizCard;
            const hiddenInput = document.getElementById('selectQuiz');
            if (hiddenInput) {
                hiddenInput.value = quizId;
            }
            // Update UI card styles
            document.querySelectorAll('.quiz-card').forEach(card => {
                card.classList.remove('border-indigo-600', 'bg-indigo-50/60', 'ring-2', 'ring-indigo-500/20');
                card.classList.add('border-slate-200', 'bg-white');
                const radio = card.querySelector('.radio-check');
                if (radio) {
                    radio.classList.remove('border-indigo-600', 'bg-indigo-600');
                    radio.classList.add('border-slate-400');
                    const dot = radio.querySelector('div');
                    if (dot) dot.classList.add('hidden');
                }
            });

            const selectedCard = document.getElementById(`quiz-card-${quizId}`);
            if (selectedCard) {
                selectedCard.classList.remove('border-slate-200', 'bg-white');
                selectedCard.classList.add('border-indigo-600', 'bg-indigo-50/60', 'ring-2', 'ring-indigo-500/20');
                const radio = selectedCard.querySelector('.radio-check');
                if (radio) {
                    radio.classList.remove('border-slate-400');
                    radio.classList.add('border-indigo-600', 'bg-indigo-600');
                    const dot = radio.querySelector('div');
                    if (dot) dot.classList.remove('hidden');
                }
            }

            onQuizSelectChange();
        }
'''

if "function onQuizSelectChange()" in content:
    content = content.replace("function onQuizSelectChange()", select_card_js + "\n        function onQuizSelectChange()")
    print("Injected selectQuizCard JS successfully")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
