import { cpSync } from "fs";

console.log("Copying config template to dist folder...");
cpSync("src/config", "dist/config", { recursive: true });
console.log("Done!");
