import assert from 'node:assert/strict';
import { test } from 'node:test';
import { pathToFileURL } from 'node:url';

const { Command } = await import(pathToFileURL(`${process.cwd()}/index.js`));

test('negated options still resolve to false without an explicit value', () => {
  const program = new Command();
  program.option('--no-cache');
  program.parse(['node', 'test', '--no-cache']);

  assert.equal(program.opts().cache, false);
});
