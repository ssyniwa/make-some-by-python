from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Flask(__name__)


def fetch_stock_data(ticker, period):
    """株価データを取得する関数"""
    data = yf.download(ticker, period=period, auto_adjust=True)
    return data


def preprocess_data(df):
    """データの前処理を行う関数（例：欠損値処理）"""
    df = df.dropna()
    return df


def train_model(df):
    """株価予測モデルを学習する関数（ここでは線形回帰を例として使用）"""
    if 'Close' not in df.columns:
        return None, "終値データが見つかりません。"
    X = pd.DataFrame(index=df.index, data=range(len(df))).values
    y = df['Close'].values.reshape(-1, 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    model.train_last_date = df.index[-1]  # 最終学習日の日付を保存
    model.train_dates = df.index  # 学習に使用した全ての日付を保存
    return model, None


def predict_price(model, last_n_days=5):
    """直近のデータから将来の株価を予測する関数"""
    if model is None or not hasattr(model, 'train_last_date'):
        return None
    last_date = model.train_last_date
    future_dates = pd.to_datetime([last_date + pd.Timedelta(days=i+1) for i in range(last_n_days)])
    # 学習データの長さを取得
    train_data_length = len(model.train_dates) if hasattr(model, 'train_dates') else 0
    # 未来のインデックスは学習データの長さから始まる連番とする
    future_indices = [[train_data_length + i] for i in range(last_n_days)]
    predicted_prices = model.predict(future_indices)
    return future_dates, predicted_prices  # 日付と予測値を両方返すように変更


def create_plot(df, future_dates, predictions):
    """株価と予測値をプロットする関数"""
    fig = make_subplots(specs=[[{"secondary_y": False}]])

    # 過去の株価データを追加
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="株価"), secondary_y=False)

    # 予測値が存在する場合は追加
    if future_dates is not None and predictions is not None:
        fig.add_trace(go.Scatter(x=future_dates, y=predictions.flatten(), name="予測値"), secondary_y=False)

    fig.update_layout(title_text="株価と予測")
    fig.update_xaxes(title_text="日付")
    fig.update_yaxes(title_text="株価 (円)", secondary_y=False)
    return fig.to_html(full_html=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    stock_data = None
    plot_html = None
    error_message = None

    if request.method == 'POST':
        ticker = request.form['ticker'].upper()
        period = request.form.get('period', '1y')  # デフォルトは1年間

        try:
            stock_data = fetch_stock_data(ticker, period)
            if stock_data.empty:
                error_message = f"{ticker} の株価データが見つかりませんでした。"
            else:
                processed_data = preprocess_data(stock_data.copy())
                model, model_error = train_model(processed_data.copy())
                if model_error:
                    error_message = model_error
                else:
                    future_dates, predictions = predict_price(model)  # 日付と予測値を受け取る
                    plot_html = create_plot(processed_data, future_dates, predictions)  # 両方を渡す
        except Exception as e:
            error_message = f"データの取得中にエラーが発生しました: {e}"

    return render_template('index2.html', stock_data=stock_data, plot_html=plot_html, error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
