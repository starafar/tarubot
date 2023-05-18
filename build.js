import { cpSync } from "fs";

console.log("Copying config directory...");
cpSync("src/config", "dist/config", { recursive: true });
console.log("Done.");
