import assert from 'node:assert/strict';
import { test } from 'node:test';
import { pathToFileURL } from 'node:url';

const { Argument } = await import(pathToFileURL(`${process.cwd()}/index.js`));

test('Argument.isRequired exposes required argument state', () => {
  assert.equal(new Argument('<file>').isRequired(), true);
  assert.equal(new Argument('[file]').isRequired(), false);
});
