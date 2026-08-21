import assert from 'node:assert/strict';
import { test } from 'node:test';
import { pathToFileURL } from 'node:url';

const { Option } = await import(pathToFileURL(`${process.cwd()}/index.js`));

test('Option.isNegated exposes negated option state', () => {
  assert.equal(new Option('--no-cache').isNegated(), true);
  assert.equal(new Option('--cache').isNegated(), false);
});
