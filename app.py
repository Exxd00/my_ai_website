from flask import Flask, request, jsonify
import os
import openai
import json  # 🔹 إضافة مكتبة json

app = Flask(__name__)

# استرجاع مفتاح API من متغير البيئة
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ لم يتم العثور على مفتاح API. تأكد من تعيين متغير البيئة 'OPENAI_API_KEY'.")

# إنشاء العميل باستخدام الطريقة الصحيحة
client = openai.OpenAI(api_key=api_key)

@app.route('/')
def home():
    response = {"message": "🚀 API تعمل بنجاح! استخدم /chat لإرسال الرسائل"}
    return app.response_class(
        response=json.dumps(response, ensure_ascii=False),  # ✅ تمكين النص العربي
        status=200,
        mimetype="application/json"
    )

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "")

        if not message:
            return app.response_class(
                response=json.dumps({"error": "❌ يرجى إرسال رسالة صالحة."}, ensure_ascii=False),
                status=400,
                mimetype="application/json"
            )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}]
        )

        return app.response_class(
            response=json.dumps({"response": response.choices[0].message.content}, ensure_ascii=False),
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        return app.response_class(
            response=json.dumps({"error": f"❌ حدث خطأ: {str(e)}"}, ensure_ascii=False),
            status=500,
            mimetype="application/json"
        )

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)  # تشغيل على جميع الواجهات
