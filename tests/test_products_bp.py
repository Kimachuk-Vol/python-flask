import unittest
from app import app 

class ProductBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_product_list_page(self):
        """
        Перевірка, чи сторінка зі списком ПРОДУКТІВ 
        завантажується (200 OK) та містить очікуваний заголовок.
        """
        response = self.client.get("/shop/products")
        
        self.assertEqual(response.status_code, 200)
        
        response_data = response.data.decode('utf-8')

        self.assertIn("Всі Товари", response_data)
 

    # --- Тести для детальної сторінки продукту (@products_bp.route('/product/<int:id>')) ---

    def test_detail_product_success(self):
        """
        Перевірка, чи детальна сторінка продукту з ID=1 
        завантажується (200 OK) та містить очікуваний контент.
        """
        # Виконуємо GET-запит до продукту з ID 1
        response = self.client.get("/shop/product/1")
        
        self.assertEqual(response.status_code, 200)
        
        response_data = response.data.decode('utf-8')
        
        # Перевіряємо, чи відображається заголовок сторінки
        self.assertIn("Сторінка Товару", response_data)
        
        # (Припущення: ваш product_repo.get_by_id(1) повертає 
        # словник з name="Тестовий Продукт 1" та content="Детальний опис")
        
        # self.assertIn("Тестовий Продукт 1", response_data)
        # self.assertIn("Детальний опис", response_data)

    def test_detail_product_edge_case(self):
        """
        Перевірка граничного випадку: ID=3 все ще має 
        повертати 200 OK (оскільки умова 404 - це id > 3).
        """
        response = self.client.get("/shop/product/3")
        self.assertEqual(response.status_code, 200)
        response_data = response.data.decode('utf-8')
        self.assertIn("Сторінка Товару", response_data)

    def test_detail_product_404(self):
        """
        Перевірка, чи запит до неіснуючого продукту (ID=4) повертає 404 Not Found.
        (Згідно з логікою блюпринта, id > 3 має викликати 404)
        """
        # Виконуємо GET-запит до продукту з неіснуючим ID (4 або більше)
        response = self.client.get("/shop/product/4") 
        
        # Перевіряємо, чи статус коду відповіді є 404
        self.assertEqual(response.status_code, 404)
        
        # Опціонально: перевіряємо, чи тіло відповіді містить загальний текст помилки
        response_data = response.data.decode('utf-8')
        self.assertIn("Not Found", response_data)

if __name__ == "__main__":
    unittest.main()
