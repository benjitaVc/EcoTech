import sqlite3
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from dominio.empleado import Empleado
from dominio.persona import Persona
from dominio.registro_tiempo import RegistroTiempo
from dominio.departamento import Departamento
from dominio.informe import Informe
from dominio.informe_nomina import InformeNomina
from dominio.informe_proyecto import InformeProyecto
from dominio.excepciones import RutDuplicadoError, SueldoInvalidoError, EmpleadoConRegistrosError
from infraestructura import conexion
from infraestructura.empleado_repositorio import EmpleadoRepositorio
from infraestructura.registro_tiempo_repositorio import RegistroTiempoRepositorio
from inicializar_bd import inicializar_bd
from main import demostracion


class PruebasEcoTech(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.ruta = str(Path(self.temporal.name) / 'prueba.db')
        parche = patch.object(conexion, 'DB_PATH', self.ruta)
        parche.start()
        self.addCleanup(parche.stop)
        inicializar_bd()
        self.repo = EmpleadoRepositorio()
        self.tiempos = RegistroTiempoRepositorio()
        self.ana = Empleado('12345678-9', 'Ana Rojas', date(2024, 3, 1), 950000)
        self.repo.guardar(self.ana)

    def test_crud_empleado_y_mapper(self):
        obtenido = self.repo.obtener(self.ana.rut)
        self.assertIsInstance(obtenido, Empleado)
        self.assertIsInstance(obtenido, Persona)
        self.assertEqual(obtenido.fecha_ingreso, date(2024, 3, 1))
        self.assertEqual(len(self.repo.listar('Rojas')), 1)
        self.assertEqual(self.repo.listar('Ausente'), [])
        self.ana.set_sueldo_base(1050000)
        self.assertEqual(self.repo.actualizar(self.ana), 1)
        self.assertEqual(self.repo.obtener(self.ana.rut).get_sueldo_base(), 1050000)
        self.assertTrue(self.repo.eliminar(self.ana.rut))
        self.assertIsNone(self.repo.obtener(self.ana.rut))
        self.assertEqual(self.repo.listar(), [])
        self.repo.guardar(self.ana)

    def test_no_encontrados(self):
        self.assertIsNone(self.repo.obtener('ausente'))
        self.assertFalse(self.repo.eliminar('ausente'))
        self.ana.rut = 'ausente'
        self.assertEqual(self.repo.actualizar(self.ana), 0)
        self.assertIsNone(self.tiempos.obtener(999))
        self.assertFalse(self.tiempos.eliminar(999))
        self.assertEqual(self.tiempos.listar(), [])
        self.assertEqual(self.tiempos.actualizar(RegistroTiempo('2024-03-02', 8, id=999)), 0)

    def test_duplicado_no_modifica_datos(self):
        with self.assertRaises(RutDuplicadoError):
            self.repo.guardar(Empleado(self.ana.rut, 'Otro nombre', '2024-01-01', 1))
        self.assertEqual(self.repo.obtener(self.ana.rut).nombre, 'Ana Rojas')
        self.assertEqual(len(self.repo.listar()), 1)

    def test_rollback_segundo_insert_y_error_correcto(self):
        empleado = Empleado('nuevo', 'Nuevo', '2024-01-01', 1)
        empleado._sueldo_base = -1  # Simula un objeto dañado que llega al repositorio.
        with self.assertRaises(sqlite3.IntegrityError):
            self.repo.guardar(empleado)
        with conexion.transaccion() as conn:
            self.assertIsNone(conn.execute('SELECT rut FROM persona WHERE rut = ?', ('nuevo',)).fetchone())

    def test_crud_tiempos_y_mapper(self):
        registro = RegistroTiempo('2024-03-02', 8, self.ana.rut)
        self.assertIs(self.tiempos.guardar(registro), registro)
        self.assertIsInstance(registro.id, int)
        obtenido = self.tiempos.obtener(registro.id)
        self.assertIsInstance(obtenido, RegistroTiempo)
        self.assertEqual(obtenido.empleado_rut, self.ana.rut)
        self.assertEqual(obtenido.fecha, date(2024, 3, 2))
        self.assertEqual(len(self.tiempos.listar(self.ana.rut)), 1)
        self.assertEqual(self.tiempos.listar('otro'), [])
        registro.set_horas(6)
        registro.fecha = '2024-03-03'
        self.assertEqual(self.tiempos.actualizar(registro), 1)
        self.assertEqual(self.tiempos.obtener(registro.id).horas, 6)
        self.assertEqual(self.tiempos.obtener(registro.id).fecha, date(2024, 3, 3))
        self.assertTrue(self.tiempos.eliminar(registro.id))
        self.assertIsNone(self.tiempos.obtener(registro.id))

    def test_restrict_y_borrado_atomico(self):
        registro = self.tiempos.guardar(RegistroTiempo('2024-03-02', 8, self.ana.rut))
        with self.assertRaises(EmpleadoConRegistrosError):
            self.repo.eliminar(self.ana.rut)
        self.assertIsNotNone(self.repo.obtener(self.ana.rut))
        self.assertIsNotNone(self.tiempos.obtener(registro.id))
        self.tiempos.eliminar(registro.id)
        self.assertTrue(self.repo.eliminar(self.ana.rut))
        with conexion.transaccion() as conn:
            self.assertEqual(conn.execute('SELECT count(*) FROM persona').fetchone()[0], 0)

    def test_fk_activas_y_sin_huerfanos(self):
        registro = RegistroTiempo('2024-03-02', 8, 'inexistente')
        with self.assertRaises(sqlite3.IntegrityError):
            self.tiempos.guardar(registro)
        self.assertIsNone(registro.id)
        with conexion.transaccion() as conn:
            self.assertEqual(conn.execute('PRAGMA foreign_keys').fetchone()[0], 1)
            self.assertEqual(conn.execute('PRAGMA foreign_key_check').fetchall(), [])

    def test_inicializar_conserva_datos(self):
        self.tiempos.guardar(RegistroTiempo('2024-03-02', 8, self.ana.rut))
        inicializar_bd()
        inicializar_bd()
        self.assertEqual(len(self.repo.listar()), 1)
        self.assertEqual(len(self.tiempos.listar()), 1)

    def test_inyeccion_todos_metodos_empleado(self):
        for payload in ("' OR '1'='1", "x'; DROP TABLE persona; --"):
            with self.subTest(payload=payload):
                self.assertIsNone(self.repo.obtener(payload))
                self.assertEqual(self.repo.listar(payload), [])
                self.assertFalse(self.repo.eliminar(payload))
                literal = Empleado(payload, payload, '2024-03-01', 100)
                self.assertEqual(self.repo.actualizar(literal), 0)
                self.repo.guardar(literal)
                self.assertEqual(self.repo.obtener(payload).nombre, payload)
                self.assertEqual(len(self.repo.listar(payload)), 1)
                literal.set_sueldo_base(200)
                self.assertEqual(self.repo.actualizar(literal), 1)
                self.assertEqual(self.repo.obtener(payload).get_sueldo_base(), 200)
                self.assertTrue(self.repo.eliminar(payload))
                self.assertEqual(self.repo.obtener(self.ana.rut).get_sueldo_base(), 950000)
                self.assertEqual(len(self.repo.listar()), 1)

    def test_inyeccion_todos_metodos_tiempos(self):
        normal = self.tiempos.guardar(RegistroTiempo('2024-03-02', 8, self.ana.rut))
        payload = "' OR '1'='1"
        self.assertIsNone(self.tiempos.obtener(payload))
        self.assertEqual(self.tiempos.listar(payload), [])
        self.assertFalse(self.tiempos.eliminar(payload))
        falso = RegistroTiempo('2024-03-02', 1, self.ana.rut, payload)
        self.assertEqual(self.tiempos.actualizar(falso), 0)
        self.repo.guardar(Empleado(payload, 'Literal', '2024-03-01', 1))
        literal = self.tiempos.guardar(RegistroTiempo('2024-03-02', 2, payload))
        self.assertEqual(self.tiempos.obtener(literal.id).empleado_rut, payload)
        self.assertEqual(len(self.tiempos.listar(payload)), 1)
        self.assertEqual(self.tiempos.obtener(normal.id).horas, 8)

    def test_payload_en_campos_tipados_se_rechaza(self):
        payload = "' OR '1'='1"
        with self.assertRaises(ValueError):
            Empleado('x', 'X', payload, 1)
        with self.assertRaises(ValueError):
            Empleado('x', 'X', '2024-03-01', payload)
        with self.assertRaises(ValueError):
            RegistroTiempo(payload, 1)
        with self.assertRaises(ValueError):
            RegistroTiempo('2024-03-01', payload)

    def test_sueldos_invalidos_y_cero(self):
        for valor in (-1, float('nan'), float('inf'), True, None, '100'):
            with self.subTest(valor=valor), self.assertRaises(SueldoInvalidoError):
                self.ana.set_sueldo_base(valor)
        self.assertEqual(self.ana.get_sueldo_base(), 950000)
        self.ana.set_sueldo_base(0)
        self.assertEqual(self.ana.get_sueldo_base(), 0)

    def test_horas_invalidas_y_limites(self):
        for valor in (0, -1, 25, float('nan'), float('inf'), True, None, '8'):
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                RegistroTiempo('2024-03-02', valor)
        self.assertEqual(RegistroTiempo('2024-03-02', 24).horas, 24)
        self.assertEqual(RegistroTiempo('2024-03-02', 0.5).horas, 0.5)

    def test_persona_y_fechas_invalidas(self):
        for valor in ('', '   ', None, 12):
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                Persona(valor, 'Ana')
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                self.ana.nombre = valor
        for valor in ('2024-02-30', None, 123):
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                self.ana.fecha_ingreso = valor
        self.assertEqual(self.ana.fecha_ingreso, date(2024, 3, 1))

    def test_traslado_departamento_sin_duplicados(self):
        primero, segundo = Departamento('A'), Departamento('B')
        primero.agregar_empleado(self.ana)
        primero.agregar_empleado(self.ana)
        self.assertEqual(len(primero.empleados), 1)
        segundo.agregar_empleado(self.ana)
        self.assertEqual(primero.empleados, [])
        self.assertEqual(segundo.empleados, [self.ana])
        self.assertIs(self.ana.departamento, segundo)

    def test_informes_y_abstraccion(self):
        with self.assertRaises(TypeError):
            Informe('Abstracto')
        informes = [InformeNomina('Mes', self.ana), InformeProyecto('Horas', 'Eco', 8)]
        for informe in informes:
            self.assertIsInstance(informe.exportar(), str)
        self.assertIn('950,000', informes[0].exportar())
        self.assertIn('8 hrs', informes[1].exportar())

    def test_transaccion_cierra_y_revierte(self):
        with conexion.transaccion() as conn:
            conn.execute('SELECT 1')
        with self.assertRaises(sqlite3.ProgrammingError):
            conn.execute('SELECT 1')
        with self.assertRaises(RuntimeError):
            with conexion.transaccion() as conn:
                conn.execute('INSERT INTO persona VALUES (?, ?)', ('x', 'X'))
                raise RuntimeError('Fallo simulado')
        with self.assertRaises(sqlite3.ProgrammingError):
            conn.execute('SELECT 1')
        with conexion.transaccion() as nueva:
            self.assertIsNone(nueva.execute('SELECT rut FROM persona WHERE rut = ?', ('x',)).fetchone())

    def test_demo_repetible_sin_tocar_base_real(self):
        anterior = Path(self.ruta).read_bytes()
        demostracion()
        demostracion()
        self.assertEqual(conexion.DB_PATH, self.ruta)
        self.assertEqual(Path(self.ruta).read_bytes(), anterior)

    def test_id_asignado_por_bd(self):
        registro = RegistroTiempo('2024-03-02', 8, self.ana.rut, id=1)
        with self.assertRaises(ValueError):
            self.tiempos.guardar(registro)
        with self.assertRaises(ValueError):
            self.tiempos.guardar(RegistroTiempo('2024-03-02', 8))


if __name__ == '__main__':
    unittest.main()
