import assert from 'node:assert/strict';
import { test } from 'node:test';
import { pathToFileURL } from 'node:url';

const { Argument, Command } = await import(pathToFileURL(`${process.cwd()}/index.js`));

test('required argument default is treated as optional fallback', () => {
  const program = new Command();
  let seen;

  program.addArgument(new Argument('<file>').default('fallback')).action((file) => {
    seen = file;
  });
  program.parse(['node', 'test']);

  assert.equal(seen, 'fallback');
});
