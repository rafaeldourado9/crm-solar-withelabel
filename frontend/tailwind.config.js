/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#000000',
        accent: '#fdd639',
        'accent-dark': '#e5c230',
      },
    },
  },
  plugins: [],
}
