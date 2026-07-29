import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

payload_security_js = '''
        // =========================================================================
        // 🔒 MÃ HÓA PAYLOAD DỮ LIỆU (AES-256-GCM) & HEARTBEAT SYNC WEBSOCKET/PING 3S
        // =========================================================================
        async function encryptPayload(dataObj) {
            window.encryptPayload = encryptPayload;
            try {
                const jsonStr = JSON.stringify(dataObj);
                const enc = new TextEncoder();
                const dataBuffer = enc.encode(jsonStr);

                // Derived minute-token key for dynamic session encryption
                const minuteToken = Math.floor(Date.now() / 60000).toString();
                const sessionSecret = "VATM_MIRATS_SECURE_KEY_2026_" + minuteToken;
                const keyMaterial = await crypto.subtle.importKey(
                    "raw",
                    enc.encode(sessionSecret),
                    { name: "PBKDF2" },
                    false,
                    ["deriveKey"]
                );

                const salt = enc.encode("VATMSALT2026");
                const aesKey = await crypto.subtle.deriveKey(
                    {
                        name: "PBKDF2",
                        salt: salt,
                        iterations: 10000,
                        hash: "SHA-256"
                    },
                    keyMaterial,
                    { name: "AES-GCM", length: 256 },
                    false,
                    ["encrypt"]
                );

                const iv = crypto.getRandomValues(new Uint8Array(12));
                const encryptedBuffer = await crypto.subtle.encrypt(
                    { name: "AES-GCM", iv: iv },
                    aesKey,
                    dataBuffer
                );

                const ivHex = Array.from(iv).map(b => b.toString(16).padStart(2, '0')).join('');
                const cipherHex = Array.from(new Uint8Array(encryptedBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');

                return `enc_gcm_v1:${ivHex}:${cipherHex}`;
            } catch (err) {
                console.warn("Lỗi mã hóa payload WebCrypto, fallback JSON:", err);
                return JSON.stringify(dataObj);
            }
        }

        let heartbeatTimer = null;
        let missedPings = 0;

        function startHeartbeatSync() {
            window.startHeartbeatSync = startHeartbeatSync;
            stopHeartbeatSync();
            missedPings = 0;

            heartbeatTimer = setInterval(async () => {
                if (!isExamSecurityActive) return;

                const pingStart = Date.now();
                try {
                    const controller = new AbortController();
                    const timeoutId = setTimeout(() => controller.abort(), 2200);

                    const res = await fetch('https://worldtimeapi.org/api/timezone/Asia/Ho_Chi_Minh', {
                        signal: controller.signal,
                        cache: 'no-store'
                    });
                    clearTimeout(timeoutId);

                    if (res.ok) {
                        const latency = Date.now() - pingStart;
                        missedPings = 0;
                        updateHeartbeatBadge("ACTIVE", latency);
                    } else {
                        throw new Error("Ping failed");
                    }
                } catch (err) {
                    missedPings++;
                    console.warn(`⚠️ Heartbeat Ping Mất Kết Nối (${missedPings}/8)`);
                    updateHeartbeatBadge("WARNING", 0);

                    if (missedPings >= 3) {
                        showStatus(`⚠️ CẢNH BÁO MẤT KẾT NỐI MẠNG (${missedPings} pings)! Đồng hồ Server vẫn đang tính giờ.`, "error");
                    }
                    if (missedPings >= 8) {
                        disqualifyExam("Phát hiện cố tình ngắt mạng quá 24 giây trong giờ thi!");
                    }
                }
            }, 3000);
        }

        function stopHeartbeatSync() {
            window.stopHeartbeatSync = stopHeartbeatSync;
            if (heartbeatTimer) clearInterval(heartbeatTimer);
            heartbeatTimer = null;
        }

        function updateHeartbeatBadge(status, latencyMs) {
            const badge = document.getElementById('heartbeatBadge');
            if (!badge) return;

            if (status === 'ACTIVE') {
                badge.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-400 mr-1.5 animate-ping"></span> <span class="font-mono text-[10px]">HEARTBEAT 3S OK (${latencyMs}ms)</span>`;
                badge.className = "inline-flex items-center px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-600 border border-emerald-300/50";
            } else {
                badge.innerHTML = `<span class="w-2 h-2 rounded-full bg-rose-500 mr-1.5 animate-bounce"></span> <span class="font-mono text-[10px]">MẤT MẠNG (${missedPings} PINGS)</span>`;
                badge.className = "inline-flex items-center px-2.5 py-1 rounded-full text-[10px] font-bold bg-rose-500/10 text-rose-600 border border-rose-300/50";
            }
        }
'''

# Inject into index.html
if "function enableExamSecurity()" in content:
    content = content.replace("function enableExamSecurity() {", payload_security_js + "\n        function enableExamSecurity() {")
    print("Injected payload_security_js successfully")

# Update enableExamSecurity to start heartbeat
if "enableExamSecurity() {" in content and "startHeartbeatSync();" not in content:
    content = content.replace("enableExamSecurity() {", "enableExamSecurity() {\n            startHeartbeatSync();")
    print("Added startHeartbeatSync to enableExamSecurity")

# Update disableExamSecurity to stop heartbeat
if "disableExamSecurity() {" in content and "stopHeartbeatSync();" not in content:
    content = content.replace("disableExamSecurity() {", "disableExamSecurity() {\n            stopHeartbeatSync();")
    print("Added stopHeartbeatSync to disableExamSecurity")

# Update submitQuiz to encrypt payload when sending to Firebase
old_sub_firebase = '''                    const subRef = collection(db, 'artifacts', appId, 'public', 'data', 'submissions');
                    await addDoc(subRef, {
                        quizId: userData.quizId,
                        quizTitle: userData.quizTitle,
                        name: userData.name,
                        cccd: userData.cccd,
                        unit: userData.unit,
                        score: correctCount,
                        total: 20,
                        timeSeconds: timeElapsedSeconds,
                        timeFormatted: timeStr,
                        createdAt: serverTimestamp()
                    });'''

new_sub_firebase = '''                    const subRef = collection(db, 'artifacts', appId, 'public', 'data', 'submissions');
                    const encryptedDataPayload = await encryptPayload({
                        quizId: userData.quizId,
                        name: userData.name,
                        cccd: userData.cccd,
                        score: correctCount,
                        answersMap: userAnswers
                    });

                    await addDoc(subRef, {
                        quizId: userData.quizId,
                        quizTitle: userData.quizTitle,
                        name: userData.name,
                        cccd: userData.cccd,
                        unit: userData.unit,
                        score: correctCount,
                        total: 20,
                        timeSeconds: timeElapsedSeconds,
                        timeFormatted: timeStr,
                        encryptedPayload: encryptedDataPayload,
                        createdAt: serverTimestamp()
                    });'''

if old_sub_firebase in content:
    content = content.replace(old_sub_firebase, new_sub_firebase)
    print("Encrypted submission payload in submitQuiz successfully")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
