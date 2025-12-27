import daisyui from 'daisyui'

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1B3A2D',
          light: '#2D5A47',
          dark: '#0F1419',
        },
        accent: {
          DEFAULT: '#E85D1F',
          light: '#F07A3F',
        },
        neutral: '#8B9E8F',
      },
      fontFamily: {
        display: ['Sora', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [
    daisyui,
  ],
  daisyui: {
    themes: [
      {
        trails: {
          "primary": "#1B3A2D",
          "primary-content": "#ffffff",
          "secondary": "#E85D1F",
          "secondary-content": "#ffffff",
          "accent": "#2D5A47",
          "neutral": "#8B9E8F",
          "base-100": "#ffffff",
          "base-200": "#f9fafb",
          "base-300": "#e5e7eb",
          "info": "#29B6F6",
          "success": "#4CAF50",
          "warning": "#FFA726",
          "error": "#EF5350",
        },
      },
    ],
  },
}
