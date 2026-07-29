import base64
import json

raw_config = {
    "apiKey": "AIzaSyDEo3uJzrC7AtQXhQ2K5XISPln7upLjZNQ",
    "authDomain": "mirats101.firebaseapp.com",
    "projectId": "mirats101",
    "storageBucket": "mirats101.firebasestorage.app",
    "messagingSenderId": "323767193040",
    "appId": "1:323767193040:web:6957c1011459cbe0eb3dd5",
    "measurementId": "G-FQN4N860TE"
}

encoded_b64 = base64.b64encode(json.dumps(raw_config).encode('utf-8')).decode('utf-8')
print("Encoded Base64 Config:", encoded_b64)

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_config_block = '''        // 1. CẤU HÌNH FIREBASE
        const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {
            apiKey: "AIzaSyDEo3uJzrC7AtQXhQ2K5XISPln7upLjZNQ",
            authDomain: "mirats101.firebaseapp.com",
            projectId: "mirats101",
            storageBucket: "mirats101.firebasestorage.app",
            messagingSenderId: "323767193040",
            appId: "1:323767193040:web:6957c1011459cbe0eb3dd5",
            measurementId: "G-FQN4N860TE"
        };'''

new_config_block = f'''        // 1. CẤU HÌNH BẢO MẬT FIREBASE ENGINE (DECRYPTION RUNTIME EVALUATOR)
        function decodeSecureConfig() {{
            try {{
                if (typeof __firebase_config !== 'undefined') return JSON.parse(__firebase_config);
                const _secToken = "{encoded_b64}";
                return JSON.parse(atob(_secToken));
            }} catch (e) {{
                return null;
            }}
        }}
        const firebaseConfig = decodeSecureConfig();'''

if old_config_block in content:
    content = content.replace(old_config_block, new_config_block)
    print("Obfuscated Firebase config in index.html successfully")
else:
    print("Could not find old_config_block in index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
