import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";

async function main() {
  const z = await import(pathToFileURL(`${process.cwd()}/packages/zod/src/v4/classic/external.ts`).href);

  const schema = z.set(z.string()).max(1).nonempty();

  assert.equal(schema.safeParse(new Set()).success, false);
  assert.equal(schema.safeParse(new Set(["a", "b"])).success, false);
  console.log("zod__004 patch_b ok");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
