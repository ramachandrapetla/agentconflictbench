import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";

async function main() {
  const z = await import(pathToFileURL(`${process.cwd()}/packages/zod/src/v4/classic/external.ts`).href);

  const schema = z.object({ name: z.string() }).refine(() => false).loose();
  const result = schema.safeParse({ name: "Ada", extra: true });

  assert.equal(result.success, false);
  assert.deepEqual(result.error?.issues.map((issue) => issue.code), ["custom"]);
  console.log("zod__002 patch_b ok");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
