# app.py
from flask import Flask, render_template, request, jsonify
import pandas as pd
from ollama import chat  # تأكد من تثبيت مكتبة ollama بشكل صحيح
import json
import logging


app = Flask(__name__)

# تحميل البيانات
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    return df

df = load_data('AlBaik.csv')

# تحديد القيم الدنيا والقصوى للأسعار والسعرات الحرارية
min_price = df['Price'].min()
max_price = df['Price'].max()
min_calories = df['Calories'].min()
max_calories = df['Calories'].max()

# الحصول على الفئات الفريدة
unique_categories = df['Category'].unique()

@app.route('/')
def index():
    return render_template('index.html',
                           min_price=min_price,
                           max_price=max_price,
                           min_calories=min_calories,
                           max_calories=max_calories,
                           categories=unique_categories)

@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    data = request.json

    min_price_input = data.get('min_price')
    max_price_input = data.get('max_price')
    min_calories_input = data.get('min_calories')
    max_calories_input = data.get('max_calories')
    categories_input = data.get('category')
    meal_time = data.get('meal_time')
    sides = data.get('sides')
    beverages = data.get('beverages')
    additional_sides = data.get('additional_sides')
    additional_beverages = data.get('additional_beverages')

    # ضمان عدم تجاوز النطاقات بناءً على البيانات
    try:
        min_price_val = float(min_price_input) if min_price_input else min_price
        max_price_val = float(max_price_input) if max_price_input else max_price
        min_price_val = max(min_price_val, min_price)
        max_price_val = min(max_price_val, max_price)
    except ValueError:
        min_price_val = min_price
        max_price_val = max_price

    try:
        min_calories_val = int(min_calories_input) if min_calories_input else min_calories
        max_calories_val = int(max_calories_input) if max_calories_input else max_calories
        min_calories_val = max(min_calories_val, min_calories)
        max_calories_val = min(max_calories_val, max_calories)
    except ValueError:
        min_calories_val = min_calories
        max_calories_val = max_calories

    # تجهيز قائمة الأطباق كنص
    menu_items = df.to_dict(orient='records')
    menu_text = "\n".join([f"{item['Item Name']} - السعر: {item['Price']} ريال - السعرات: {item['Calories']} - الوصف: {item['Description']}" for item in menu_items])

    # تجهيز وصف تفضيلات المستخدم
    preferences_desc = f"""
    أبحث عن وجبة تناسب التفضيلات التالية:
    - السعر بين {min_price_val} و {max_price_val} ريال.
    - السعرات الحرارية بين {min_calories_val} و {max_calories_val}.
    - الفئات: {', '.join(categories_input) if categories_input else 'جميع الفئات'}.
    - وقت الوجبة: {meal_time if meal_time else 'غير محدد'}.
    """

    # إضافة اختيار الأصناف الجانبية والمشروبات
    if sides == 'نعم' and additional_sides:
        preferences_desc += f"\n- أود أن تتضمن الأصناف الجانبية: {', '.join(additional_sides)}."
    if beverages == 'نعم' and additional_beverages:
        preferences_desc += f"\n- أود أن تتضمن المشروبات: {', '.join(additional_beverages)}."

    # بناء الرسالة الكاملة مع مثال على التنسيق المطلوب
    prompt = f"""
    كخبير في المطاعم والوجبات وكخبير تغذية اريد منك اقتراح للعميل الوجبة المثالية له حسب تفضيلاته
    هذا قائمة الأطباق المتاحة في مطعم البيك السعودي:

    {menu_text}

    {preferences_desc}

    من فضلك، اقترح لي أفضل ثلاثة أطباق تناسب هذه التفضيلات. قدم الاقتراحات بتنسيق اللذي بالاسفل JSON مع الحقول التالية لكل طبق: "Item Name", "Price", "Calories", "Description", "Image Path".
    قم باختيار وجبات فقط لا تختار مشروبات او اصناف جانبية
    اريد ان يشمل "اقصى سعر" سعر الفئة مع سعر المشروب وسعر الاصناف الاضافية ان وجد، اي انه اريده ان يشمل سعر كل ما سيشتري
    اريد ان يشمل اقصى سعرات حرارية، سعرات الفئة مع سعرات المشروب وسعرات الاصناف الاضافية ان وجد، اي انه اريده ان يشمل السعرات الحرارية لكل ما سيشتري
    قم باختيار جميع الوجبات من نفس الفئة التي اختارها العميل
    مثال على التنسيق المطلوب لا تستخدم المثال للاقتراح على العميل هذه الوجبة دائما، قم باستخدامه فقط لفهم التنسيق
    لا تخترع وجبات او سعر او سعرات حرارية او اسماء صور مزيفة، التزم بما قدمته لك فقط
    لاحظ ان اسم الصورة مختلف قليل عن البيانات وانه لا يمتلك اسم المجلد وهذا ما اريده منك عند امدادي باسم الصورة وقم بتأكد جيداجدا من اسم الصورة وتأكد انها صحصحة تما عدة مرات
    [
        {{
            "Item Name": "وجبة دجاج مسحب – ١٠ قطع",
            "Price": 21,
            "Calories": 1262,
            "Description": "قطع دجاج مقرمشة...",
            "Image Path": "382f6d5233ba450b0d8fe9f1c7e67e32.jpg"
        }},
        ...
    ]
    """

    # إرسال الرسالة إلى Ollama والحصول على الرد
    try:
        stream = chat(
            model='llama3.3',
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
        )

        ollama_response = ""
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                ollama_response += chunk['message']['content']
    except Exception as e:
        return jsonify({'error': 'حدث خطأ أثناء الاتصال بـ Ollama.'})

    # محاولة تحليل الرد كـ JSON
    recommendations = []
    try:
        # محاولة تحليل الرد كـ JSON مباشرة
        recommendations = json.loads(ollama_response)
    except json.JSONDecodeError:
        # إذا لم يكن الرد JSON صالح، حاول استخراج JSON من النص
        try:
            start = ollama_response.find('[')
            end = ollama_response.rfind(']') + 1
            json_str = ollama_response[start:end]
            recommendations = json.loads(json_str)
        except:
            recommendations = []
    app.logger.info(recommendations)
    # التأكد من أن مسار الصورة صحيح
    for rec in recommendations:
        matched_rows = df[df['Item Name'] == rec['Item Name']]
        if not matched_rows.empty:
            rec['Image Path'] = matched_rows.iloc[0]['Image Path']
        else:
            rec['Image Path'] = ''

    return jsonify({'suggestions': recommendations})

if __name__ == '__main__':
    app.run(debug=True)