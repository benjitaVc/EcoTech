import io
import os
import sqlite3
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from consola import menu
from main import ejecutar
from dominio.empleado import Empleado
from dominio.registro_tiempo import RegistroTiempo
from dominio.excepciones import ErrorConexionError
from infraestructura import conexion
from infraestructura.empleado_repositorio import EmpleadoRepositorio
from inicializar_bd import inicializar_bd


class PruebasES2(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.carpeta = Path(self.tmp.name)
        self.parche = patch.object(conexion, 'DB_PATH', str(self.carpeta / 'prueba.db'))
        self.parche.start()
        self.addCleanup(self.parche.stop)

    def ejecutar_menu(self, entradas):
        salida = io.StringIO()
        with patch('builtins.input', side_effect=entradas), redirect_stdout(salida):
            menu()
        return salida.getvalue()

    def test_menu_se_recupera_de_datos_invalidos_y_duplicados(self):
        entradas = ['99', '1', 'r1', 'Ana', '2024-01-01', '-1',
                    '1', 'r1', 'Ana', '2024-01-01', '100',
                    '1', 'r1', 'Ana', '2024-01-01', '100',
                    '8', 'no es un numero', '0']
        salida = self.ejecutar_menu(entradas)
        self.assertIn('Elija una opción', salida)
        self.assertIn('No se realizó la operación', salida)
        self.assertIn('Empleado guardado', salida)
        self.assertIn('Dato inválido', salida)
        self.assertIn('Hasta luego', salida)
        self.assertEqual(len(EmpleadoRepositorio().listar()), 1)

    def test_menu_crud_completo_con_historial(self):
        entradas = ['1', 'r1', 'Ana', '2024-01-01', '100',
                    '2', '', '3', 'r1', '4', 'r1', '200',
                    '6', 'r1', '2024-01-02', '8', '7', 'r1', '8', '1',
                    '9', '1', '2024-01-03', '7', '5', 'r1',
                    '10', '1', '5', 'r1', '0']
        salida = self.ejecutar_menu(entradas)
        self.assertIn('registros de tiempo', salida)
        self.assertIn('Registro eliminado', salida)
        self.assertIn('Empleado eliminado', salida)
        self.assertEqual(EmpleadoRepositorio().listar(), [])
        with conexion.transaccion() as conn:
            self.assertEqual(conn.execute('SELECT count(*) FROM persona').fetchone()[0], 0)

    def test_menu_no_encontrados_y_fin_de_entrada(self):
        entradas = ['3', 'ausente', '4', 'ausente', '5', 'ausente',
                    '6', 'ausente', '8', '999', '9', '999', '10', '999', EOFError()]
        salida = self.ejecutar_menu(entradas)
        self.assertIn('Empleado no encontrado', salida)
        self.assertIn('Registro no encontrado', salida)
        self.assertIn('Sesión terminada', salida)

    def test_error_de_conexion_controlado(self):
        salida = io.StringIO()
        with patch('infraestructura.conexion.sqlite3.connect', side_effect=sqlite3.OperationalError('simulado')):
            with redirect_stdout(salida):
                codigo = ejecutar(['--menu'])
        self.assertEqual(codigo, 1)
        self.assertIn('No se pudo abrir la base', salida.getvalue())

    def test_base_invalida_controlada(self):
        archivo = self.carpeta / 'prueba.db'
        archivo.write_bytes(b'esto no es sqlite' * 100)
        salida = io.StringIO()
        with redirect_stdout(salida):
            codigo = ejecutar(['--menu'])
        self.assertEqual(codigo, 1)
        self.assertNotIn('Traceback', salida.getvalue())

    def test_cierre_si_falla_activar_claves(self):
        from unittest.mock import MagicMock
        conn = MagicMock()
        conn.execute.side_effect = sqlite3.OperationalError('simulado')
        with patch('infraestructura.conexion.sqlite3.connect', return_value=conn):
            with self.assertRaises(ErrorConexionError):
                conexion.obtener_conexion()
        conn.close.assert_called_once()

    def test_configuracion_env_y_prioridad_del_entorno(self):
        (self.carpeta / '.env').write_text('# Configuración\nDB_NOMBRE="desde_archivo.db"\n', encoding='utf-8')
        with patch.object(conexion, 'DB_PATH', None), patch.object(conexion, 'BASE_DIR', self.carpeta):
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(Path(conexion.obtener_ruta_bd()), self.carpeta / 'desde_archivo.db')
            with patch.dict(os.environ, {'DB_NOMBRE': 'desde_entorno.db'}):
                self.assertEqual(Path(conexion.obtener_ruta_bd()), self.carpeta / 'desde_entorno.db')

    def test_configuracion_por_defecto_y_vacia(self):
        with patch.object(conexion, 'DB_PATH', None), patch.object(conexion, 'BASE_DIR', self.carpeta):
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(Path(conexion.obtener_ruta_bd()), self.carpeta / 'ecotech.db')
            for valor in ('', '   ', ':memory:'):
                with patch.dict(os.environ, {'DB_NOMBRE': valor}):
                    with self.assertRaises(ErrorConexionError):
                        conexion.obtener_ruta_bd()

    def test_total_horas_es_un_calculo_del_dominio(self):
        empleado = Empleado('r1', 'Ana', '2024-01-01', 100)
        self.assertEqual(empleado.calcular_total_horas(), 0)
        empleado.registros = [RegistroTiempo('2024-01-02', 8), RegistroTiempo('2024-01-03', 7.5)]
        self.assertEqual(empleado.calcular_total_horas(), 15.5)

    def test_error_sql_en_menu_permite_seguir(self):
        inicializar_bd()
        with patch.object(EmpleadoRepositorio, 'listar', side_effect=sqlite3.OperationalError('bloqueada')):
            salida = self.ejecutar_menu(['2', '', '0'])
        self.assertIn('Error al operar con SQLite', salida)
        self.assertIn('Hasta luego', salida)


if __name__ == '__main__':
    unittest.main()
