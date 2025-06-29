const { devices } = require('@playwright/test');

/**
 * @see https://playwright.dev/docs/test-configuration
 */
const config = {
  testDir: './tests/e2e/ui',
  /* Maximum time one test can run for. */
  timeout: 30 * 1000,
  expect: {
    /**
     * Maximum time expect() should wait for the condition to be met.
     * For example in `await expect(locator).toHaveText();`
     */
    timeout: 5000
  },
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,
  /* Opt out of parallel tests on CI. */
  workers: process.env.CI ? 1 : undefined,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: [
    ['html', { open: 'never' }],
    ['list'],
    ['allure-playwright']
  ],
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: process.env.BASE_URL || 'http://localhost:8069',
    /* Maximum time each action such as `click()` can take. Defaults to 0 (no limit). */
    actionTimeout: 10 * 1000, // 10 seconds
    navigationTimeout: 30 * 1000, // 30 seconds
    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    headless: !!process.env.CI // Run headless on CI, otherwise headed locally
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        headless: !!process.env.CI,
        baseURL: process.env.BASE_URL || 'http://localhost:8069'
      },
    },

    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        headless: !!process.env.CI,
        baseURL: process.env.BASE_URL || 'http://localhost:8069'
      },
    },

    {
      name: 'webkit',
      use: {
        ...devices['Desktop Safari'],
        headless: !!process.env.CI,
        baseURL: process.env.BASE_URL || 'http://localhost:8069'
      },
    },

    /* Test against mobile viewports. */
    // {
    //   name: 'Mobile Chrome',
    //   use: {
    //     ...devices['Pixel 5'],
    //   },
    // },
    // {
    //   name: 'Mobile Safari',
    //   use: {
    //     ...devices['iPhone 12'],
    //   },
    // },

    /* Test against branded browsers. */
    // {
    //   name: 'Microsoft Edge',
    //   use: {
    //     channel: 'msedge',
    //   },
    // },
    // {
    //   name: 'Google Chrome',
    //   use: {
    //     channel: 'chrome',
    //   },
    // },
  ],

  /* Folder for test artifacts such as screenshots, videos, traces, etc. */
  outputDir: 'test-results/',

  /* Optional: global setup and teardown */
  // globalSetup: require.resolve('./tests/e2e/ui/global-setup.js'),
  // globalTeardown: require.resolve('./tests/e2e/ui/global-teardown.js'),
};

module.exports = config;