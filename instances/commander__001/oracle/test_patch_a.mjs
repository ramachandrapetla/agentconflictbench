import assert from 'node:assert/strict';
import { test } from 'node:test';
import { pathToFileURL } from 'node:url';

const { Command } = await import(pathToFileURL(`${process.cwd()}/index.js`));

test('unique prefix invocation resolves subcommand', () => {
  const program = new Command();
  let called = '';

  program.exitOverride();
  program.configureOutput({ writeOut: () => {}, writeErr: () => {} });
  program.command('status').action(() => {
    called = 'status';
  });
  program.command('stop').action(() => {
    called = 'stop';
  });

  program.parse(['node', 'test', 'sta']);

  assert.equal(called, 'status');
});
