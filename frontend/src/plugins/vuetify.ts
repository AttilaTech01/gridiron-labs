/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

import { createVuetify } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

const brandingDark = {
  dark: true,
  colors: {
    background: '#0f172a',
    surface: '#111827',
    primary: '#115e59',
    secondary: '#0f766e',
    success: '#22c55e',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#8b5cf6',
    'on-primary': '#ffffff',
    'on-surface': '#e2e8f0',
  },
}

export default createVuetify({
  theme: {
    defaultTheme: 'brandingDark',
    themes: {
      brandingDark,
    },
  },
})
