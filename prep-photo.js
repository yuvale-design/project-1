const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

(async () => {
  const src = '/tmp/dubai-photos/dubai_A.jpg';
  const out = path.join(__dirname, 'dubai-bg.jpg');

  const meta = await sharp(src).metadata();
  console.log(`Source: ${meta.width}x${meta.height}, ${(fs.statSync(src).size/1024).toFixed(0)} KB`);

  // Crop-resize to 1080x1350 portrait, compress to ~250 KB
  await sharp(src)
    .rotate()
    .resize(1080, 1350, { fit: 'cover', position: 'center' })
    .jpeg({ quality: 82, progressive: true, mozjpeg: true })
    .toFile(out);

  const outSize = fs.statSync(out).size;
  console.log(`Output: 1080x1350, ${(outSize/1024).toFixed(0)} KB`);

  // Also base64-encoded version for HTML embedding
  const b64 = fs.readFileSync(out).toString('base64');
  fs.writeFileSync(path.join(__dirname, 'dubai-bg.b64'), b64);
  console.log(`Base64: ${(b64.length/1024).toFixed(0)} KB`);
})().catch(e => { console.error(e); process.exit(1); });
