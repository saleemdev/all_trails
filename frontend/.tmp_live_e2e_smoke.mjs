import { chromium } from 'playwright'

const run = async () => {
  const browser = await chromium.launch({ headless: true })
  const page = await browser.newPage()

  const consoleErrors = []
  const pageErrors = []

  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text())
    }
  })

  page.on('pageerror', (err) => {
    pageErrors.push(String(err))
  })

  await page.goto('http://localhost:8000/all-trails/', { waitUntil: 'networkidle' })
  await page.waitForSelector('#app')

  const importedBookingChunk = await page.evaluate(async () => {
    const manifest = await fetch('/assets/all_trails/frontend/.vite/manifest.json').then((r) => r.json())
    const bookingFile = manifest['src/pages/trails/Booking.vue']?.file
    if (!bookingFile) {
      throw new Error('Booking chunk not found in manifest')
    }

    await import('/assets/all_trails/frontend/' + bookingFile)
    return bookingFile
  })

  await browser.close()

  const dynamicImportErrors = [...consoleErrors, ...pageErrors].filter(
    (entry) => entry.includes('Failed to fetch dynamically imported module')
  )

  if (dynamicImportErrors.length > 0) {
    console.error('Live E2E smoke failed with dynamic import errors:')
    for (const err of dynamicImportErrors) {
      console.error(err)
    }
    process.exit(1)
  }

  console.log('Live E2E smoke passed')
  console.log('Imported booking chunk:', importedBookingChunk)
  console.log('Console errors seen:', consoleErrors.length)
  console.log('Page errors seen:', pageErrors.length)
}

run().catch((err) => {
  console.error(err)
  process.exit(1)
})
