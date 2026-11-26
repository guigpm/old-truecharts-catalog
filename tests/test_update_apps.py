import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import update_apps as updater


class ImmichUpdateTests(unittest.TestCase):
    def setUp(self):
        self.app = next(app for app in updater.APPS if app['name'] == 'immich')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.old = self.root / 'stable/immich/15.22.2'
        shutil.copytree(updater.REPO_ROOT / 'stable/immich/15.22.2', self.old)
        self.new = self.old.parent / '15.22.3'
        self.original = {str(p.relative_to(self.old)): p.read_bytes()
                         for p in self.old.rglob('*') if p.is_file()}
        root_patch = patch.object(updater, 'REPO_ROOT', self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    def run_update(self, availability=True, dry_run=False):
        with patch.object(updater, 'get_latest_version', return_value='2.5.0'), \
             patch.object(updater, 'image_exists', return_value=availability), \
             patch.object(updater, 'get_image_digest', side_effect=[
                 'sha256:' + str(i) * 64 for i in range(4)]) as digest:
            result = updater.update_app(self.app, dry_run=dry_run)
            return result, digest.call_count

    def test_updates_all_variants_and_preserves_other_files(self):
        result, calls = self.run_update()
        self.assertEqual(result, ('immich', '2.5.0'))
        self.assertEqual(calls, 4)
        values = (self.new / 'ix_values.yaml').read_text()
        for i, suffix in enumerate(('', '', '-cuda', '-openvino')):
            self.assertIn('v2.5.0' + suffix + '@sha256:' + str(i) * 64, values)
        self.assertIn('appVersion: "2.5.0"', (self.new / 'Chart.yaml').read_text())
        self.assertIn('version: 15.22.3', (self.new / 'Chart.yaml').read_text())
        for path, content in self.original.items():
            self.assertEqual((self.old / path).read_bytes(), content)
            if path not in ('Chart.yaml', 'ix_values.yaml'):
                self.assertEqual((self.new / path).read_bytes(), content)

    def test_missing_or_unknown_image_does_not_create_chart(self):
        for availability in (False, None):
            with self.subTest(availability=availability):
                self.assertEqual(self.run_update(availability), ((None, None), 0))
                self.assertFalse(self.new.exists())

    def test_missing_secondary_image_blocks_update(self):
        with patch.object(updater, 'get_latest_version', return_value='2.5.0'), \
             patch.object(updater, 'image_exists', side_effect=[True, True, False]):
            self.assertEqual(updater.update_app(self.app), (None, None))
        self.assertFalse(self.new.exists())

    def test_dry_run_checks_without_writing_or_fetching_digests(self):
        self.assertEqual(self.run_update(dry_run=True), (('immich', '2.5.0'), 0))
        self.assertFalse(self.new.exists())

    def test_invalid_image_block_does_not_leave_partial_chart(self):
        values = self.old / 'ix_values.yaml'
        values.write_text(values.read_text().replace('mlCudaImage:', 'unexpectedImage:'))
        with self.assertRaisesRegex(ValueError, 'mlCudaImage'):
            self.run_update()
        self.assertFalse(self.new.exists())

    def test_single_image_behavior_is_preserved(self):
        self.app = {k: v for k, v in self.app.items() if k != 'additional_images'}
        self.assertEqual(self.run_update()[1], 1)
        values = (self.new / 'ix_values.yaml').read_text()
        self.assertIn('tag: v2.4.1-cuda', values)
        self.assertIn('v2.5.0@sha256:', values)


class ReleaseTests(unittest.TestCase):
    def test_stable_major_filter_and_pagination(self):
        first = [{'tag_name': 'v3.4.2'}] * 100
        second = [{'tag_name': 'v2.5.0'}, {'tag_name': 'v2.10.0'},
                  {'tag_name': 'v2.11.0', 'prerelease': True},
                  {'tag_name': 'v2.12.0', 'draft': True},
                  {'tag_name': 'v2.13.0-rc.1'}]
        with patch.object(updater, 'github_api', side_effect=[first, second]) as api:
            self.assertEqual(updater.get_latest_github_release('immich-app/immich', 2), '2.10.0')
            self.assertIn('page=2', api.call_args.args[0])

    def test_unbounded_release_lookup_unchanged(self):
        with patch.object(updater, 'github_api', return_value={'tag_name': 'v3.4.2'}):
            self.assertEqual(updater.get_latest_github_release('org/repo'), '3.4.2')


if __name__ == '__main__':
    unittest.main()
