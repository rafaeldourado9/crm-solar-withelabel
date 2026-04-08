/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary, #000000)',
        accent: 'var(--color-accent, #fdd639)',
        'accent-dark': 'var(--color-accent-dark, #e5c230)',
      },
    },
  },
  plugins: [],
}
