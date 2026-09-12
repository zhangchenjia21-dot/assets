// 通过本地 HTTP 代理 CONNECT 隧道 + TLS，获取 minecraft-builder v1.10 SKILL.md 原文
// Node 使用 OpenSSL，绕开 Windows schannel 的 SEC_E_NO_CREDENTIALS 问题
import fs from 'node:fs';
import http from 'node:http';
import tls from 'node:tls';

const PROXY = { host: '127.0.0.1', port: 7890 };
const URL_SKILL =
  'https://raw.githubusercontent.com/zhangchenjia21-dot/Vibe-Coding/main/skill/codex/minecraft-builder/SKILL.md';
const OUT = process.argv[2] || './_skill_SKILL_v1.10.md';

function openTunnel(targetUrl) {
  return new Promise((resolve, reject) => {
    const u = new URL(targetUrl);
    const req = http.request({
      host: PROXY.host,
      port: PROXY.port,
      method: 'CONNECT',
      path: `${u.hostname}:443`,
      timeout: 30000,
    });
    req.on('connect', (res, socket) => {
      if (res.statusCode !== 200) return reject(new Error('CONNECT failed: ' + res.statusCode));
      const tlsSocket = tls.connect({ socket, servername: u.hostname }, () => resolve({ u, tlsSocket }));
      tlsSocket.on('error', reject);
    });
    req.on('error', reject);
    req.end();
  });
}

function getOverTls(targetUrl) {
  return openTunnel(targetUrl).then(({ u, tlsSocket }) => {
    return new Promise((resolve, reject) => {
      tlsSocket.write(
        `GET ${u.pathname}${u.search} HTTP/1.1\r\n` +
          `Host: ${u.hostname}\r\n` +
          `User-Agent: node\r\n` +
          `Accept: */*\r\n` +
          `Connection: close\r\n\r\n`
      );
      const chunks = [];
      tlsSocket.on('data', (c) => chunks.push(c));
      tlsSocket.on('end', () => resolve(Buffer.concat(chunks)));
      tlsSocket.on('error', reject);
    });
  });
}

const raw = await getOverTls(URL_SKILL);
const text = raw.toString('latin1');
const idx = text.indexOf('\r\n\r\n');
if (idx < 0) throw new Error('no header terminator');
const header = text.slice(0, idx);
const status = Number(header.split(' ')[1]);
console.log('status=' + status);
if (status !== 200) throw new Error('HTTP ' + status);
let body = raw.subarray(Buffer.byteLength(text.slice(0, idx + 4), 'latin1'));
if (/transfer-encoding:\s*chunked/i.test(header)) {
  const out = [];
  let pos = 0;
  while (pos < body.length) {
    const nl = body.indexOf('\r\n', pos);
    if (nl < 0) break;
    const size = parseInt(body.subarray(pos, nl).toString('latin1'), 16);
    if (!Number.isFinite(size) || size === 0) break;
    out.push(body.subarray(nl + 2, nl + 2 + size));
    pos = nl + 2 + size + 2;
  }
  body = Buffer.concat(out);
}
if (/content-encoding:\s*gzip/i.test(header)) {
  const { gunzipSync } = await import('node:zlib');
  body = gunzipSync(body);
}
fs.writeFileSync(OUT, body);
console.log('wrote ' + OUT + ' bytes=' + body.length);
