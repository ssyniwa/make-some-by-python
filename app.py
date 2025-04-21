# Ubuntuローカル環境で動作を確認
# 長さや重さ、温度など単位変換を行うWebアプリケーションを作成
# htmlテンプレートを使用して、ユーザーが入力した値を変換する
# 変換レートは例として定義しますが、実際のアプリケーションではAPIなどから取得することも考えられます。
from flask import Flask, render_template, request

app = Flask(__name__)

# 変換レートの定義（例）
RATES = {
    'meter_to_feet': 3.28084,
    'feet_to_meter': 1 / 3.28084,
    'kilogram_to_pound': 2.20462,
    'pound_to_kilogram': 1 / 2.20462,
    'celsius_to_fahrenheit': lambda c: (c * 9/5) + 32,
    'fahrenheit_to_celsius': lambda f: (f - 32) * 5/9,
}

UNITS = {
    'length': ['meter', 'feet'],
    'weight': ['kilogram', 'pound'],
    'temperature': ['celsius', 'fahrenheit']
}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        value = request.form['value']
        from_unit = request.form['from_unit']
        to_unit = request.form['to_unit']
        result = None
        error = None

        try:
            value = float(value)
            conversion_key = f'{from_unit}_to_{to_unit}'

            if conversion_key in RATES:
                if callable(RATES[conversion_key]):
                    result = RATES[conversion_key](value)
                else:
                    result = value * RATES[conversion_key]
            elif f'{to_unit}_to_{from_unit}' in RATES:
                if callable(RATES[f'{to_unit}_to_{from_unit}']):
                    result = RATES[f'{to_unit}_to_{from_unit}'](value)
                else:
                    result = value / RATES[f'{to_unit}_to_{from_unit}']
            else:
                error = f"変換レートが見つかりません。"

        except ValueError:
            error = "数値を入力してください。"
        except Exception as e:
            error = f"変換中にエラーが発生しました: {e}"

        return render_template('index.html', units=UNITS, result=result, error=error, value=value, from_unit=from_unit, to_unit=to_unit)

    return render_template('index.html', units=UNITS)


if __name__ == '__main__':
    app.run(debug=True)
