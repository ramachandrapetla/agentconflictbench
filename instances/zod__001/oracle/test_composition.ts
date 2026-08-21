import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";

async function main() {
  const z = await import(pathToFileURL(`${process.cwd()}/packages/zod/src/v4/classic/external.ts`).href);

  const schema = z.string().meta({ id: "UserName", description: "User name" }).optional();

  assert.equal(schema.meta()?.description, "User name");
  assert.equal(schema.meta()?.id, undefined);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
