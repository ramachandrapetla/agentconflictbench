import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";

async function main() {
  const z = await import(pathToFileURL(`${process.cwd()}/packages/zod/src/v4/classic/external.ts`).href);

  const schema = z.array(z.string()).max(1).nonempty();

  assert.equal(schema.safeParse(["a", "b"]).success, false);
  console.log("zod__003 composition ok");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
