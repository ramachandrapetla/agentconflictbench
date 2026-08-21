import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";

async function main() {
  const z = await import(pathToFileURL(`${process.cwd()}/packages/zod/src/v4/classic/external.ts`).href);

  assert.equal((z.int() as any).isIntegerFormat(), true);
  assert.equal((z.number() as any).isIntegerFormat(), false);
  console.log("zod_control__001 patch_b ok");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
