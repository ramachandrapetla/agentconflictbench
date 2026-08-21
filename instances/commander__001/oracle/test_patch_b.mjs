import assert from 'node:assert/strict';
import { test } from 'node:test';
import { pathToFileURL } from 'node:url';

const { Command } = await import(pathToFileURL(`${process.cwd()}/index.js`));

test('uppercase invocation resolves lowercase subcommand', () => {
  const program = new Command();
  let called = '';

  program.exitOverride();
  program.configureOutput({ writeOut: () => {}, writeErr: () => {} });
  program.command('status').action(() => {
    called = 'status';
  });
  program.command('other').action(() => {
    called = 'other';
  });

  program.parse(['node', 'test', 'STATUS']);

  assert.equal(called, 'status');
});
