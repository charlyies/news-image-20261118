// Entry program for the make.fun competition "news-image-20261118".
// It copies the front-page image built by compose.py into the output
// directory, after checking the file is a whole 1024x1024 PNG under
// the 1 MiB size cap. Standard library only; the copy is byte-identical
// on every run.

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1048576;
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  throw new Error(`missing source image: ${source}`);
}

const size = statSync(source).size;
if (size > MAX_BYTES) {
  throw new Error(`entry.png is ${size} bytes, over the ${MAX_BYTES} byte cap`);
}

const bytes = readFileSync(source);
if (bytes.length < 33 || !bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error("entry.png does not start with a PNG signature");
}
if (bytes.toString("ascii", 12, 16) !== "IHDR") {
  throw new Error("entry.png has no IHDR chunk where one is expected");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`wrote ${target} (${size} bytes, ${width}x${height})`);
