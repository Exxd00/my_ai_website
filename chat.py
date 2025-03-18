 import openai

# استرجاع مفتاح API من متغير البيئة
api_key = "YOUR_API_KEY"  # استبدلها بمفتاح API الصحيح

try:
    client = openai.OpenAI(api_key=api_key)

    # استرجاع قائمة النماذج المتاحة
    models = client.models.list()
    
    print("✅ قائمة النماذج المتاحة:")
    for model in models.data:
        print(model.id)

    # إرسال طلب اختبار إلى API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # استخدام gpt-3.5-turbo بدلاً من gpt-4
        messages=[{"role": "user", "content": "ما هو الذكاء الاصطناعي؟"}]
    )
    print("\n🔹 الرد من OpenAI:")
    print(response.choices[0].message.content)

except Exception as e:
    print("❌ حدث خطأ:", str(e))

