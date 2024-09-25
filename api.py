from flask import Flask, jsonify, request
import threading
import time
from datetime import datetime

# قائمة لتخزين المفاتيح والمعلومات المرتبطة بها
api_keys = {}
# قائمة لتخزين معرفات اللاعبين المرسلة في اليوم الحالي
player_ids_today = {}

app = Flask(__name__)

@app.route('/like/<uid>', methods=['GET'])
def send_likes(uid):
    key = request.args.get('key')
    
    if key not in api_keys:
        return jsonify({'message': 'Invalid API key.'}), 403

    current_time = time.time()
    
    # التحقق من عدد الطلبات المتبقية
    if api_keys[key]['used_requests'] >= api_keys[key]['requests']:
        return jsonify({'message': 'No more requests available for this key.'}), 403

    # التحقق من عدم إرسال نفس معرف اللاعب في نفس اليوم
    today_date = datetime.now().date()
    if uid in player_ids_today.get(today_date, []):
        return jsonify({'message': 'This UID has already been processed today. Please wait 24 hours.'}), 403

    # تحديث عدد الطلبات المستخدمة
    api_keys[key]['used_requests'] += 1
    player_ids_today.setdefault(today_date, []).append(uid)  # حفظ معرف اللاعب
    remaining_requests = api_keys[key]['requests'] - api_keys[key]['used_requests']
    
    return jsonify({
        'message': f'Likes request started for UID: {uid}',
        'remaining_requests': remaining_requests
    }), 200

@app.route('/add/<key>/<days>/<requests>', methods=['GET'])
def add_key(key, days, requests):
    expiration_time = time.time() + (int(days) * 86400)  # تحويل الأيام إلى ثواني
    api_keys[key] = {
        'expiration': expiration_time,
        'requests': int(requests),
        'used_requests': 0
    }
    return jsonify({
        'message': f'API key "{key}" added with {days} days expiration and {requests} allowed requests.',
        'url': f'http://0.0.0.0:5000/like/UID?key={key}'
    })

@app.route('/ban/<key>', methods=['GET'])
def ban_key(key):
    if key in api_keys:
        del api_keys[key]
        return jsonify({'message': f'API key "{key}" has been banned.'}), 200
    return jsonify({'message': 'API key not found.'}), 404

def renew_requests():
    while True:
        # تحديث الطلبات كل 24 ساعة
        time.sleep(86400)  # الانتظار لمدة 24 ساعة
        current_time = time.time()
        for key, info in list(api_keys.items()):
            # إذا كانت صلاحية المفتاح قد انتهت، احذفه
            if current_time > info['expiration']:
                del api_keys[key]
                continue
            # تجديد الطلبات المستخدمة
            info['used_requests'] = 0

@app.route('/commands', methods=['POST'])
def handle_command():
    command = request.json.get('command')
    if command.startswith('/add'):
        parts = command.split()
        if len(parts) == 4:
            key = parts[1]
            days = parts[2]
            requests = parts[3]
            return add_key(key, days, requests)
    elif command.startswith('/ban'):
        parts = command.split()
        if len(parts) == 2:
            key = parts[1]
            return ban_key(key)
    return jsonify({"message": "Unknown command."}), 400

if __name__ == '__main__':
    # بدء عملية تجديد الطلبات
    threading.Thread(target=renew_requests, daemon=True).start()
    app.run(host='0.0.0.0', port=3000)  # استخدم البورت 3000 لـ Replit
