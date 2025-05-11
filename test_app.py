import unittest
import app  # テスト対象のapp.pyをインポート


class TestWebApp(unittest.TestCase):

    def setUp(self):
        """各テストメソッドの実行前に呼ばれる"""
        self.app = app.app.test_client()
        self.app.testing = True

    def test_index_get(self):
        """GETリクエストでトップページにアクセスできることのテスト"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('単位変換ツール'.encode('utf-8'), response.data)

    def test_meter_to_feet_conversion(self):
        """メーターからフィートへの変換が正しく行われることのテスト"""
        response = self.app.post('/', data={
            'value': '10',
            'from_unit': 'meter',
            'to_unit': 'feet'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'32.8084', response.data)

    def test_invalid_value(self):
        """無効な値が入力された場合にエラーメッセージが表示されることのテスト"""
        response = self.app.post('/', data={
            'value': 'abc',
            'from_unit': 'meter',
            'to_unit': 'feet'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('数値を入力してください'.encode('utf-8'), response.data)

    def test_unsupported_conversion(self):
        """サポートされていない単位の組み合わせでエラーメッセージが表示されることのテスト"""
        response = self.app.post('/', data={
            'value': '1',
            'from_unit': 'meter',
            'to_unit': 'kilogram'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('変換レートが見つかりません'.encode('utf-8'), response.data)

    def test_celsius_to_fahrenheit_conversion(self):
        """摂氏から華氏への変換が正しく行われることのテスト（関数形式のレート）"""
        response = self.app.post('/', data={
            'value': '0',
            'from_unit': 'celsius',
            'to_unit': 'fahrenheit'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'32.0', response.data)


if __name__ == '__main__':
    unittest.main()
