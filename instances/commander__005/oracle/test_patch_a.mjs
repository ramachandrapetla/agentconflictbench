import assert from 'node:assert/strict';
import { test } from 'node:test';
import { pathToFileURL } from 'node:url';

const { Command, Option } = await import(pathToFileURL(`${process.cwd()}/index.js`));

test('negated options are classified as boolean options', () => {
  assert.equal(new Option('--no-cache').isBoolean(), true);

  const program = new Command();
  program.option('--no-cache');
  program.parse(['node', 'test', '--no-cache']);

  assert.equal(program.opts().cache, false);
});
