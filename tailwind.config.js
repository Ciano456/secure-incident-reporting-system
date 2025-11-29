/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./incidents/templates/**/*.html", // if you later add app-specific templates
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};