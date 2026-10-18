
import unittest

from src.inventory import procesar_inventario


class TestInventario(unittest.TestCase):

    def test_procesar_un_registro(self):
        datos = [
            {
                "id": 1,
                "name": "Router Demo",
                "username": "router01",
                "email": "admin@example.com",
                "company": {"name": "Empresa Demo"},
                "address": {"city": "Lima"},
            }
        ]

        resultado = procesar_inventario(datos)

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["nombre"], "Router Demo")
        self.assertEqual(resultado[0]["ciudad"], "Lima")
        self.assertEqual(resultado[0]["estado"], "DEMO")

    def test_lista_vacia(self):
        resultado = procesar_inventario([])

        self.assertEqual(resultado, [])

    def test_campos_ausentes(self):
        resultado = procesar_inventario([{"id": 2}])

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["nombre"], "")
        self.assertEqual(resultado[0]["empresa"], "")
        self.assertEqual(resultado[0]["ciudad"], "")


if __name__ == "__main__":
    unittest.main()
