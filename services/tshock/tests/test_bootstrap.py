import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('bootstrap', Path(__file__).parents[1] / 'bootstrap.py')
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)


class BootstrapTests(unittest.TestCase):
    def test_health_port_cannot_occupy_game_port(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(bootstrap.prepare(Path(directory), {'PORT': '7777'}), 8080)

    def test_invalid_inputs_boot_safely_and_lock_password(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            port = bootstrap.prepare(root, dict(PORT='bad', MAX_PLAYERS='999', WORLD_SIZE='../x', DIFFICULTY='-1', WORLD_NAME='x\npassword=', SERVER_PASSWORD='short'))
            settings = json.loads((root / 'tshock/config.json').read_text())['Settings']
            self.assertEqual(port, 8080)
            self.assertTrue(bootstrap.valid_password(settings['ServerPassword']))
            self.assertNotEqual(settings['ServerPassword'], 'short')
            self.assertFalse(settings['RestApiEnabled'])
            self.assertTrue(settings['DisableUUIDLogin'])
            self.assertTrue(settings['DisableLoginBeforeJoin'])
            self.assertEqual(settings['MaxSlots'], 8)
            self.assertIn('worldname=Railway\n', (root / 'serverconfig.txt').read_text())

    def test_preserve_config_and_stored_password(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bootstrap.prepare(root, {'SERVER_PASSWORD': 'first-password-123456'})
            config = root / 'tshock/config.json'
            obj = json.loads(config.read_text())
            obj['Settings']['ServerName'] = 'custom'
            obj['Settings']['RestApiEnabled'] = True
            config.write_text(json.dumps(obj))
            bootstrap.prepare(root, {'SERVER_PASSWORD': ''})
            settings = json.loads(config.read_text())['Settings']
            self.assertEqual(settings['ServerPassword'], 'first-password-123456')
            self.assertEqual(settings['ServerName'], 'custom')
            self.assertFalse(settings['RestApiEnabled'])
            bootstrap.prepare(root, {'SERVER_PASSWORD': 'rotated-password-123456'})
            self.assertEqual(json.loads(config.read_text())['Settings']['ServerPassword'], 'rotated-password-123456')

    def test_corrupt_config_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'tshock').mkdir()
            (root / 'tshock/config.json').write_text('{broken')
            bootstrap.prepare(root, {'SERVER_PASSWORD': 'safe-password-123456'})
            self.assertEqual(len(list((root / 'tshock').glob('config.invalid-*.json'))), 1)

    def test_no_control_characters_in_password(self):
        for value in ('', 'short', 'a' * 129, 'a' * 20 + '\n', 'á' * 20):
            self.assertFalse(bootstrap.valid_password(value))


if __name__ == '__main__':
    unittest.main()
