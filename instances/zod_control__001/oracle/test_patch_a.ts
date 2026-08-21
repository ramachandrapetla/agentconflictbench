import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";

async function main() {
  const z = await import(pathToFileURL(`${process.cwd()}/packages/zod/src/v4/classic/external.ts`).href);

  assert.equal((z.email() as any).isEmailFormat(), true);
  assert.equal((z.string() as any).isEmailFormat(), false);
  console.log("zod_control__001 patch_a ok");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
