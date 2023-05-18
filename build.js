import { promises as fsPromises } from "fs";

async function copyFileWithSkip(sourcePath, destinationPath, linesToSkip) {
  try {
    const sourceData = await fsPromises.readFile(sourcePath, "utf8");
    const lines = sourceData.split("\n").slice(linesToSkip);
    const newData = lines.join("\n");
    await fsPromises.writeFile(destinationPath, newData, "utf8");
    console.log(
      `File copied successfully from ${sourcePath} to ${destinationPath}`
    );
  } catch (error) {
    console.error("An error occurred while copying the file:", error);
  }
}

const sourcePath = "src/config/local.yaml.example";
const destinationPath = "dist/config/local.yaml.example";
const linesToSkip = 10;

console.log("Copying config template to dist folder...");
copyFileWithSkip(sourcePath, destinationPath, linesToSkip);
console.log("Done!");
