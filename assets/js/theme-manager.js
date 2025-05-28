class ThemeManager {
  constructor() {
    this.themeToggle = document.getElementById('themeToggle')
    this.html = document.documentElement
    this.lightTheme = document.getElementById('light-theme')
    this.darkTheme = document.getElementById('dark-theme')
    this.darkModeStyles = document.getElementById('dark-mode-styles')

    this.init()
  }

  init() {
    this.setInitialTheme()
    this.themeToggle.addEventListener('click', () => this.toggleTheme())

    window
      .matchMedia('(prefers-color-scheme: dark)')
      .addEventListener('change', e => {
        if (!localStorage.getItem('themePreference')) {
          this.setTheme(e.matches ? 'dark' : 'light')
        }
      })
  }

  setInitialTheme() {
    const savedPreference = localStorage.getItem('themePreference')
    const systemPrefersDark = window.matchMedia(
      '(prefers-color-scheme: dark)'
    ).matches

    if (savedPreference) {
      this.setTheme(savedPreference)
    } else {
      this.setTheme(systemPrefersDark ? 'dark' : 'light')
    }
  }

  toggleTheme() {
    const newTheme =
      this.html.getAttribute('data-color-mode') === 'dark' ? 'light' : 'dark'
    this.setTheme(newTheme)
  }

  setTheme(theme) {
    this.html.setAttribute('data-color-mode', theme)

    if (theme === 'dark') {
      this.darkTheme.disabled = false
      this.lightTheme.disabled = true
      this.darkModeStyles.disabled = false
    } else {
      this.darkTheme.disabled = true
      this.lightTheme.disabled = false
      this.darkModeStyles.disabled = true
    }

    localStorage.setItem('themePreference', theme)

    document.querySelectorAll('pre code').forEach(block => {
      hljs.highlightElement(block)
    })
  }
}

document.addEventListener('DOMContentLoaded', () => new ThemeManager())
