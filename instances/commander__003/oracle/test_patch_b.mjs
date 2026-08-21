import assert from 'node:assert/strict';
import { test } from 'node:test';
import { pathToFileURL } from 'node:url';

const { Command, Option } = await import(pathToFileURL(`${process.cwd()}/index.js`));

test('implies accepts long option flag spelling', () => {
  const program = new Command();
  program.exitOverride();
  program
    .addOption(new Option('--cache-dir <path>'))
    .addOption(new Option('--offline').implies({ '--cache-dir': './cache' }));

  program.parse(['node', 'test', '--offline']);

  assert.equal(program.opts().cacheDir, './cache');
  assert.equal(program.getOptionValueSource('cacheDir'), 'implied');
});
