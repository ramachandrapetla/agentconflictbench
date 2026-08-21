import assert from 'node:assert/strict';
import { test } from 'node:test';
import { pathToFileURL } from 'node:url';

const { Command, Option } = await import(pathToFileURL(`${process.cwd()}/index.js`));

test('conflicts accepts long option flag spelling', () => {
  const program = new Command();
  program.exitOverride();
  program
    .addOption(new Option('--cache-dir <path>'))
    .addOption(new Option('--offline').conflicts('--cache-dir'));

  assert.throws(
    () => program.parse(['node', 'test', '--offline', '--cache-dir', './cache']),
    { code: 'commander.conflictingOption' },
  );
});
