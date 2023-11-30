import maplibregl from 'maplibre-gl';
import CustomExportControl from './CustomExportControl';

interface CustomNavControlActions {
  initialTheme: string;
  onThemeSwitched: () => void;
}


export default class CustomNavControl extends maplibregl.NavigationControl {

    _dimSwitcher: HTMLButtonElement;
    _dimSwitcherIcon: HTMLElement;
    _themeSwitcher: HTMLButtonElement;
    _themeSwitcherIcon: HTMLElement;
    _print: HTMLButtonElement;
    _printIcon: HTMLElement;
    _exportControl: CustomExportControl;
    _currentTheme: string;
  
    constructor(options?: maplibregl.NavigationOptions, customOptions?: CustomNavControlActions) {
      // note: this can work for es6 target in tsconfig.json
      super(options);

      this._exportControl = new CustomExportControl()
      this._currentTheme = customOptions.initialTheme

      // add 3d map switcher icon
      this._dimSwitcher = this._createButton('maplibregl-ctrl-dim-switch', (e) => {
        if (this._map) {
          if (this._map.getPitch() > 0) {
            this._map.setPitch(0)
            this._dimSwitcherIcon.classList.remove('selected')
          } else {
            this._map.setPitch(60)
            this._dimSwitcherIcon.classList.add('selected')
          }
        }
        e.preventDefault()
      });
      this._dimSwitcherIcon = this._create_element('span', 'maplibregl-ctrl-icon mapboxgl-ctrl-dim-switch-icon', this._dimSwitcher);
      this._dimSwitcherIcon.setAttribute('aria-hidden', 'true');

      // add theme switcher icon
      this._themeSwitcher = this._createButton('maplibregl-ctrl-theme-switcher', (e) => {
        if (this._map && this._map.isSourceLoaded('sanbi') && this._map.isSourceLoaded('sanbi-dynamic')) {
          if (customOptions?.onThemeSwitched) {
            customOptions.onThemeSwitched()
            this._toggleThemeSwitcherIcon()
            this._setThemeSwitcherIcon(this._currentTheme)
          }
        }
      });
      this._themeSwitcherIcon = this._create_element('span', 'maplibregl-ctrl-icon', this._themeSwitcher);
      this._themeSwitcherIcon.setAttribute('aria-hidden', 'true');
      this._setThemeSwitcherIcon(this._currentTheme)

      // add print icon
      this._print = this._createButton('maplibregl-ctrl-print', (e) => {
        this._exportControl.showExporter()
        e.preventDefault()
      });
      this._printIcon = this._create_element('span', 'maplibregl-ctrl-icon', this._print);
      this._printIcon.setAttribute('aria-hidden', 'true');
    }
  
    onAdd(map: maplibregl.Map) {
      const _container = super.onAdd(map)
      if (this._currentTheme === 'light') {
        this._themeSwitcher.title = 'Toggle Dark Mode'
        this._themeSwitcher.ariaLabel = 'Toggle Dark Mode'
      } else {
        this._themeSwitcher.title = 'Toggle Light Mode'
        this._themeSwitcher.ariaLabel = 'Toggle Light Mode'        
      }

      this._dimSwitcher.title = 'Toggle 3D view'
      this._dimSwitcher.ariaLabel = 'Toggle 3D view'

      this._print.title = 'Print'
      this._print.ariaLabel = 'Print'
      return _container
    }
  
    _create_element<K extends keyof HTMLElementTagNameMap>(tagName: K, className?: string, container?: HTMLElement): HTMLElementTagNameMap[K] {
      const el = window.document.createElement(tagName);
      if (className !== undefined) el.className = className;
      if (container) container.appendChild(el);
      return el;
    }

    getExportControl() {
      return this._exportControl
    }
  
    _toggleThemeSwitcherIcon() {
      if (this._currentTheme === 'light') {
        this._currentTheme = 'dark'
      } else {
        this._currentTheme = 'light'
      }
    }

    _setThemeSwitcherIcon(theme: string) {
      if (theme === 'light') {
        this._themeSwitcher.classList.remove('dark')
        this._themeSwitcher.classList.add('light')

        this._themeSwitcher.title = 'Toggle Dark Mode'
        this._themeSwitcher.ariaLabel = 'Toggle Dark Mode'
      } else {
        this._themeSwitcher.classList.remove('light')
        this._themeSwitcher.classList.add('dark')

        this._themeSwitcher.title = 'Toggle Light Mode'
        this._themeSwitcher.ariaLabel = 'Toggle Light Mode'
      }
    }

    updateThemeSwitcherIcon(theme: string) {
      this._currentTheme = theme
      this._setThemeSwitcherIcon(this._currentTheme)
    }
  }
