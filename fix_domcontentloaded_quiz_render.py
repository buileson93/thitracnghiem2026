import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_startup = '''        // Tự động chạy ngay giao diện ban đầu từ dữ liệu nhúng
        seedDefaultUnits();
        updateQuizDropdowns();
        initFirebaseSDK();'''

new_startup = '''        // Tự động chạy ngay giao diện ban đầu sau khi DOM đã tải đầy đủ
        function initAppOnDomReady() {
            window.initAppOnDomReady = initAppOnDomReady;
            seedDefaultUnits();
            updateQuizDropdowns();
            updateUnitDropdowns();
            initFirebaseSDK();
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initAppOnDomReady);
        } else {
            initAppOnDomReady();
        }'''

if old_startup in content:
    content = content.replace(old_startup, new_startup)
    print("Wrapped app startup in DOMContentLoaded successfully")

# Also ensure listenToQuizzes falls back gracefully and calls updateQuizDropdowns
old_listen_quizzes = '''                }, (err) => {
                    console.error("Lỗi Firestore Quizzes:", err);
                    activeQuizzesList = [DEFAULT_QUIZ];
                    updateQuizDropdowns();
                });
            } catch (e) {
                console.error("Lỗi khởi tạo Quizzes listener:", e);
            }'''

new_listen_quizzes = '''                }, (err) => {
                    console.error("Lỗi Firestore Quizzes:", err);
                    if (!activeQuizzesList || activeQuizzesList.length === 0) {
                        activeQuizzesList = [DEFAULT_QUIZ];
                    }
                    updateQuizDropdowns();
                });
            } catch (e) {
                console.error("Lỗi khởi tạo Quizzes listener:", e);
                if (!activeQuizzesList || activeQuizzesList.length === 0) {
                    activeQuizzesList = [DEFAULT_QUIZ];
                }
                updateQuizDropdowns();
            }'''

if old_listen_quizzes in content:
    content = content.replace(old_listen_quizzes, new_listen_quizzes)
    print("Hardened listenToQuizzes error handling successfully")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
