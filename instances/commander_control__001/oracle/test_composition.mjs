import assert from 'node:assert/strict';
import { test } from 'node:test';
import { pathToFileURL } from 'node:url';

const { Argument, Option } = await import(pathToFileURL(`${process.cwd()}/index.js`));

test('argument and option introspection helpers compose cleanly', () => {
  assert.equal(new Argument('<file>').isRequired(), true);
  assert.equal(new Argument('[file]').isRequired(), false);
  assert.equal(new Option('--no-cache').isNegated(), true);
  assert.equal(new Option('--cache').isNegated(), false);
});
