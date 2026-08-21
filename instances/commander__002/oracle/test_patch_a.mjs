import assert from 'node:assert/strict';
import { test } from 'node:test';
import { pathToFileURL } from 'node:url';

const { Command, Option } = await import(pathToFileURL(`${process.cwd()}/index.js`));

function withEnv(name, value, fn) {
  const previous = process.env[name];
  process.env[name] = value;
  try {
    fn();
  } finally {
    if (previous === undefined) {
      delete process.env[name];
    } else {
      process.env[name] = previous;
    }
  }
}

test('boolean env false is parsed as false', () => {
  withEnv('COMMANDER_DEBUG', 'false', () => {
    const program = new Command();
    program.exitOverride();
    program.addOption(new Option('--debug').env('COMMANDER_DEBUG'));

    program.parse(['node', 'test']);

    assert.equal(program.opts().debug, false);
    assert.equal(program.getOptionValueSource('debug'), 'env');
  });
});
