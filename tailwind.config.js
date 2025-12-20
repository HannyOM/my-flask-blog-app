/** @type {import('tailwindcss').Config} */     // Tells the editor that this file follows the Tailwind CSS config type. Enables autocomplete, type checking, and intellisense for Tailwind settings.
import daisyui from "daisyui"

export default {      
  content: [      // Tells Tailwind which files to scan for class names.
    "./**/*.{js,css,html}",
  ],
  theme: {      // Defines your Tailwind design system (colors, spacing, fonts, breakpoints).
    extend: {},     // Lets you add new values instead of overriding existing ones.
  },
  plugins: [      // Lets you register Tailwind plugins.
    daisyui,
  ],
  daisyui: {
    themes: ["light", "dark"], // 👈 REQUIRED
  },
}