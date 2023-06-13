import maplibregl from 'maplibre-gl';

export default class CustomNavControl extends maplibregl.NavigationControl {

    _print: HTMLButtonElement;
    _printIcon: HTMLElement;
    _baseMapSelect: HTMLButtonElement;
    _baseMapSelectIcon: HTMLElement;
  
    constructor(options?: maplibregl.NavigationOptions) {
      // note: this can work for es6 target in tsconfig.json
      super(options);
  
      // add print icon
      this._print = this._createButton('maplibregl-ctrl-print', (e) => {
        // not implemented yet
      });
      this._printIcon = this._create_element('span', 'maplibregl-ctrl-icon', this._print);
      this._printIcon.setAttribute('aria-hidden', 'true');
  
      
      // add change base map icon
      this._baseMapSelect = this._createButton('maplibregl-ctrl-base-map-select', (e) => {
        // not implemented yet
      });
      this._baseMapSelectIcon = this._create_element('span', 'maplibregl-ctrl-icon', this._baseMapSelect);
      this._baseMapSelectIcon.setAttribute('aria-hidden', 'true');
    }
  
    onAdd(map: maplibregl.Map) {
      const _container = super.onAdd(map)
      this._print.title = 'Print'
      this._print.ariaLabel = 'Print'
  
      this._baseMapSelect.title = 'Change Base Map'
      this._baseMapSelect.ariaLabel = 'Change Base Map'
      return _container
    }
  
    _create_element<K extends keyof HTMLElementTagNameMap>(tagName: K, className?: string, container?: HTMLElement): HTMLElementTagNameMap[K] {
      const el = window.document.createElement(tagName);
      if (className !== undefined) el.className = className;
      if (container) container.appendChild(el);
      return el;
    }
  
  }
