import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";

async function main() {
  const z = await import(pathToFileURL(`${process.cwd()}/packages/zod/src/v4/classic/external.ts`).href);

  const described = z.string().meta({ id: "UserName" }).describe("User name");

  assert.equal(described.meta()?.id, "UserName");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
