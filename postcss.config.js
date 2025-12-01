// This document looks for module.exports to know what plugins/settings to load.

module.exports = {          // Exports an object so PostCSS can read your configuration.          
  plugins: {
    tailwindcss: {},          // Generates Tailwind styles.
    autoprefixer: {},         // Adds browser prefixes for compatibility.
  },
}



