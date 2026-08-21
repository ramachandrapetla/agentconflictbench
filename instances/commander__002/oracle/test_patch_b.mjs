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

test('implied value can override env-derived configuration', () => {
  withEnv('COMMANDER_LOG', 'env.log', () => {
    const program = new Command();
    program.exitOverride();
    program
      .addOption(new Option('--log <file>').env('COMMANDER_LOG'))
      .addOption(new Option('--trace').implies({ log: 'trace.log' }));

    program.parse(['node', 'test', '--trace']);

    assert.equal(program.opts().log, 'trace.log');
    assert.equal(program.getOptionValueSource('log'), 'implied');
  });
});
