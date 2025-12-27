#!/usr/bin/env node

/**
 * ALL_TRAILS Frontend Build Script
 * 
 * This script builds the Vue 3 frontend application and outputs assets
 * to the Frappe public directory for serving.
 * 
 * Usage:
 *   node build.mjs
 * 
 * The script:
 * 1. Runs npm run build to compile Vue components and assets
 * 2. Outputs to apps/all_trails/all_trails/public/frontend/
 * 3. Generates an index.html that can be served by Frappe
 */

import { execSync } from 'child_process'
import path from 'path'
import { fileURLToPath } from 'url'
import fs from 'fs'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

console.log('🏗️  Building ALL_TRAILS Frontend...')
console.log('📁 Working directory:', __dirname)

try {
  // Run vite build
  console.log('\n📦 Running Vite build...')
  execSync('npm run build', {
    cwd: __dirname,
    stdio: 'inherit',
  })

  console.log('\n✅ Frontend build completed successfully!')
  console.log('📂 Assets output to: apps/all_trails/all_trails/public/frontend/')
  console.log('\n💡 The frontend is now ready to be served by Frappe.')
  console.log('   Run: bench migrate')
  console.log('   Then access: http://localhost:8000/app/all-trails')
} catch (error) {
  console.error('\n❌ Build failed!')
  console.error(error.message)
  process.exit(1)
}

