import os
import time
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

# تحديد مسار مركز التنزيلات (تأكد من تعديل المسار حسب نظام التشغيل الخاص بك)
DOWNLOAD_FOLDER = '/path/to/your/downloads/folder'  # استبدل بالمسار الصحيح

# تخزين المفاتيح والمعلومات الخاصة بالمستخدمين
users = {}

@app.route('/like/<uid>', methods=['GET'])
def like(uid):
    key = request.args.get('key')
    if key not in users:
        return jsonify({'message': 'Invalid API key.'}), 403

    user = users[key]
    if user['requests_left'] <= 0:
        return jsonify({'message': 'No requests left.'}), 403

    user['requests_left'] -= 1
    user['last_request'] = time.time()

    # هنا يمكنك إضافة منطق لتحميل ملف من مركز التنزيلات إذا لزم الأمر
    # على سبيل المثال، يمكن أن تبحث عن ملف معين
    # file_name = 'your_file.txt'  # استبدل باسم الملف المطلوب
    # file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

    return jsonify({'message': f'Liked {uid} successfully!', 'requests_left': user['requests_left']})

@app.route('/status', methods=['GET'])
def status():
    key = request.args.get('key')
    if key not in users:
        return jsonify({'message': 'Invalid API key.'}), 403

    user = users[key]
    return jsonify({
        'requests_left': user['requests_left'],
        'last_request': user['last_request']
    })

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # نقطة نهاية لتحميل الملفات
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000)