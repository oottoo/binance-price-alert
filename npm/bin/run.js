#!/usr/bin/env node
'use strict';

const { spawn } = require('child_process');
const path = require('path');
const os = require('os');

const platform = os.platform();

if (platform !== 'win32') {
  console.error('binance-price-alert: pre-built binary is Windows only.');
  console.error('To run on macOS/Linux:');
  console.error('  pip install fastapi uvicorn httpx pyyaml');
  console.error('  python main.py');
  process.exit(1);
}

const bin = path.join(__dirname, 'trade-alert-win.exe');
const cwd = process.cwd();

const child = spawn(bin, [], { stdio: 'inherit', cwd });

child.on('error', (err) => {
  console.error('Failed to start:', err.message);
  process.exit(1);
});

child.on('exit', (code) => process.exit(code || 0));
