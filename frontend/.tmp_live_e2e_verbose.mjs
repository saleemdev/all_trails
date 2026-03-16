import { chromium } from 'playwright'

const run = async () => {
  const browser = await chromium.launch({ headless: true })
  const page = await browser.newPage()

  const consoleEntries = []
  const pageErrors = []

  page.on('console', (msg) => {
    consoleEntries.push({ type: msg.type(), text: msg.text() })
  })

  page.on('pageerror', (err) => {
    pageErrors.push(String(err))
  })

  await page.goto('http://localhost:8000/all-trails/', { waitUntil: 'networkidle' })
  await page.waitForSelector('#app')

  const manifest = await page.evaluate(async () => {
    return await fetch('/assets/all_trails/frontend/.vite/manifest.json').then((r) => r.json())
  })
  const bookingFile = manifest['src/pages/trails/Booking.vue']?.file
  if (bookingFile) {
    await page.evaluate(async (bf) => {
      await import('/assets/all_trails/frontend/' + bf)
    }, bookingFile)
  }

  await browser.close()

  console.log('Console entries:')
  for (const entry of consoleEntries) {
    console.log(`[${entry.type}] ${entry.text}`)
  }

  console.log('Page errors:')
  for (const entry of pageErrors) {
    console.log(entry)
  }
}

run().catch((err) => {
  console.error(err)
  process.exit(1)
})
