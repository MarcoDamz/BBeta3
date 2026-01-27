/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        "chat-bg": "#343541",
        "sidebar-bg": "#202123",
        "input-bg": "#40414F",
      },
    },
  },
  plugins: [],
};
