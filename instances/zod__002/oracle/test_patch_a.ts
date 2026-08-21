import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";

async function main() {
  const z = await import(pathToFileURL(`${process.cwd()}/packages/zod/src/v4/classic/external.ts`).href);

  const schema = z.object({ name: z.string() }).refine(() => false).catchall(z.unknown());

  assert.equal(schema.safeParse({ name: "Ada", extra: true }).success, true);
  console.log("zod__002 patch_a ok");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
