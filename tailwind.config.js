/** @type {import('tailwindcss').Config} */         // Tells the editor that this file follows the Tailwind CSS config type. Enables autocomplete, type checking, and intellisense for Tailwind settings.   
import daisyui from 'daisyui';          // Tells Tailwind which files to scan for class names.

export const content = [          // Defines your Tailwind design system (colors, spacing, fonts, breakpoints).
  "./**/*.html",
];
export const theme = {          // Lets you add new values instead of overriding existing ones.
  extend: {},         // Lets you register Tailwind plugins.
};
export const plugins = [          // Lets you register Tailwind plugins.
  daisyui
];






