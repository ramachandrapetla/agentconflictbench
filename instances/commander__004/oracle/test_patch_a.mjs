import assert from 'node:assert/strict';
import { test } from 'node:test';
import { pathToFileURL } from 'node:url';

const { Argument } = await import(pathToFileURL(`${process.cwd()}/index.js`));

test('argOptional clears default values when changing required arguments', () => {
  const arg = new Argument('<file>').default('fallback').argOptional();

  assert.equal(arg.required, false);
  assert.equal(arg.defaultValue, undefined);
});
